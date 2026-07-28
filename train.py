import argparse
import json
import math
import random
import numpy as np
import torch
import matplotlib

# Use a non-interactive backend so plots can be saved without a display
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from game import LunarLanderEnv
from agent import Agent

# --- Effective training configuration ---
ALGORITHM = "vanilla"
SEED = 43
NUM_EPISODES = 1000
LEARNING_RATE = 5e-4
TARGET_UPDATE_FREQ = 2000
REPLAY_BUFFER_CAPACITY = 10_000
BATCH_SIZE = 64
GAMMA = 0.99
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train a deterministic Vanilla or Double DQN agent.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--algorithm",
        choices=("vanilla", "double_dqn"),
        default=ALGORITHM,
    )
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--episodes", type=int, default=NUM_EPISODES)
    parser.add_argument(
        "--learning-rate", type=float, default=LEARNING_RATE
    )
    parser.add_argument(
        "--target-update-freq",
        "--target-update-frequency",
        dest="target_update_freq",
        type=int,
        default=TARGET_UPDATE_FREQ,
    )
    parser.add_argument(
        "--epsilon-start", type=float, default=EPSILON_START
    )
    parser.add_argument("--epsilon-min", type=float, default=EPSILON_MIN)
    parser.add_argument("--epsilon-decay", type=float, default=EPSILON_DECAY)
    parser.add_argument(
        "--replay-capacity", type=int, default=REPLAY_BUFFER_CAPACITY
    )
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--gamma", type=float, default=GAMMA)
    args = parser.parse_args()

    if args.seed < 0:
        parser.error("--seed must be non-negative")
    if args.episodes <= 0:
        parser.error("--episodes must be positive")
    if not math.isfinite(args.learning_rate) or args.learning_rate <= 0:
        parser.error("--learning-rate must be positive")
    if args.target_update_freq <= 0:
        parser.error("--target-update-freq must be positive")
    if args.replay_capacity <= 0:
        parser.error("--replay-capacity must be positive")
    if args.batch_size <= 0:
        parser.error("--batch-size must be positive")
    if args.replay_capacity < args.batch_size:
        parser.error("--replay-capacity must be at least --batch-size")
    if not 0.0 <= args.gamma <= 1.0:
        parser.error("--gamma must be between 0 and 1")
    if not 0.0 <= args.epsilon_min <= args.epsilon_start <= 1.0:
        parser.error(
            "epsilon values must satisfy "
            "0 <= --epsilon-min <= --epsilon-start <= 1"
        )
    if not 0.0 < args.epsilon_decay <= 1.0:
        parser.error("--epsilon-decay must be greater than 0 and at most 1")

    return args


ARGS = parse_args()
ALGORITHM = ARGS.algorithm
SEED = ARGS.seed
NUM_EPISODES = ARGS.episodes
LEARNING_RATE = ARGS.learning_rate
TARGET_UPDATE_FREQ = ARGS.target_update_freq
REPLAY_BUFFER_CAPACITY = ARGS.replay_capacity
BATCH_SIZE = ARGS.batch_size
GAMMA = ARGS.gamma
EPSILON_START = ARGS.epsilon_start
EPSILON_MIN = ARGS.epsilon_min
EPSILON_DECAY = ARGS.epsilon_decay

# Use disjoint, explicit RNG streams. Training episode seeds are
# 20000 + SEED through that base plus NUM_EPISODES - 1. Hold-out collection
# uses its own environment and separate 30000 + SEED / 40000 + SEED streams.
TRAIN_ENV_SEED_BASE = 20_000 + SEED
TRAIN_ACTION_SPACE_SEED = 21_000 + SEED
HOLDOUT_ENV_SEED_BASE = 30_000 + SEED
HOLDOUT_ACTION_SPACE_SEED = 40_000 + SEED

# Seed the process-level RNGs used by epsilon-greedy action selection, replay
# sampling, NumPy operations, and PyTorch initialization/learning.
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# Window used for the moving-average reward curve (training metric).
MOVING_AVG_WINDOW = 50
# Evaluate average max Q-value on the hold-out states every N episodes.
Q_EVAL_EVERY = 10
HOLDOUT_STATE_COUNT = 200

# --- Greedy validation checkpoint selection ---
# The training moving-average reward is an epsilon-greedy metric; it measures
# learning progress under exploration noise, not deployment quality. To select
# weights.pth by the same mode test.py uses, we periodically run a small,
# non-rendered greedy evaluation (epsilon=0) and checkpoint on its mean reward.
VALIDATE_EVERY = 50          # run validation every N training episodes
VALIDATION_EPISODES = 10     # number of greedy eval episodes per validation
VALIDATION_BASE_SEED = 901   # validation seeds 901.. (kept SEPARATE from the
                             # 1234+ diagnostic/test seeds so checkpoint
                             # selection never optimises against test data)
SOLVED_THRESHOLD = 200.0     # reward >= this counts as "solved"; tie-break only

WEIGHTS_PATH = "weights.pth"
METRICS_PATH = "training_metrics.json"
PLOT_PATH = "training_plot.png"


def moving_average(values, window):
    """Trailing moving average; the first (window-1) entries are averaged over
    fewer elements so the curve is defined from the first episode."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.empty(n, dtype=float)
    for i in range(n):
        lo = max(0, i - window + 1)
        out[i] = values[lo:i + 1].mean()
    return out


def run_greedy_validation(agent, episodes, base_seed):
    """Evaluation-only greedy rollout. It does NOT replace, bypass, or alter
    epsilon-greedy action selection in training: it uses a direct deterministic
    argmax (the exact code path agent.act() takes at epsilon=0 / test time)
    WITHOUT calling agent.act(), so no random.random() exploration draw is
    consumed and the Python/NumPy/PyTorch RNG sequences of training are left
    untouched. No transitions are added to the Replay Buffer, agent.epsilon is
    never mutated, and no learning/optimizer step is performed. Uses a SEPARATE
    non-rendered env and validation-only seeds so checkpoint selection never
    sees test seeds."""
    val_env = LunarLanderEnv()
    policy_net = agent.policy_net
    try:
        rewards = []
        with torch.no_grad():
            for i in range(episodes):
                state = val_env.reset(seed=base_seed + i)
                done = False
                total = 0.0
                while not done:
                    state_t = torch.as_tensor(state, dtype=torch.float32).unsqueeze(0)
                    q_values = policy_net(state_t)
                    action = int(q_values.argmax(dim=1).item())
                    state, reward, done = val_env.step(action)
                    total += reward
                rewards.append(total)
        rewards = np.asarray(rewards, dtype=float)
        return {
            "mean_reward": float(np.mean(rewards)),
            "median_reward": float(np.median(rewards)),
            "std_reward": float(np.std(rewards)),
            "solved_rate": float(np.mean(rewards >= SOLVED_THRESHOLD)),
            "rewards": rewards.tolist(),
        }
    finally:
        val_env.close()


# Initialize the environment
env = LunarLanderEnv()
env.action_space.seed(TRAIN_ACTION_SPACE_SEED)
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

# Initialize the agent with every experimental hyperparameter explicit.
agent = Agent(action_size=action_size,
              state_size=state_size,
              batch_size=BATCH_SIZE,
              replay_buffer_capacity=REPLAY_BUFFER_CAPACITY,
              gamma=GAMMA,
              epsilon_start=EPSILON_START,
              epsilon_end=EPSILON_MIN,
              epsilon_decay=EPSILON_DECAY,
              lr=LEARNING_RATE,
              target_update_freq=TARGET_UPDATE_FREQ,
              algorithm=ALGORITHM)

# --- Hold-out States Collection ---
# Use a separate, fully seeded environment so diagnostic state collection
# cannot consume or alter the training environment's RNG state.
hold_out_env = LunarLanderEnv()
hold_out_env.action_space.seed(HOLDOUT_ACTION_SPACE_SEED)
hold_out_states = []
hold_out_reset_count = 0
state = hold_out_env.reset(seed=HOLDOUT_ENV_SEED_BASE)

for _ in range(HOLDOUT_STATE_COUNT):
    action = hold_out_env.action_space.sample()  # Take a seeded random action
    next_state, reward, done = hold_out_env.step(action)
    hold_out_states.append(state)
    state = next_state
    if done:
        hold_out_reset_count += 1
        state = hold_out_env.reset(
            seed=HOLDOUT_ENV_SEED_BASE + hold_out_reset_count
        )

# Convert hold-out states to tensor for fast evaluation later
hold_out_states_tensor = torch.FloatTensor(np.array(hold_out_states))
hold_out_env.close()

# Lists to keep track of rewards and average max Q-values for reporting
episode_rewards = []
average_q_values = []         # average max Q over hold-out states (per Q_EVAL_EVERY episodes)
average_q_episodes = []       # episode index aligned with average_q_values

# Best-checkpoint selection is driven by greedy validation mean reward
# (deployment quality), not the epsilon-greedy training moving average.
validation_history = []       # list of dicts, one per validation run
best_val_mean = -float('inf')
best_val_solved = -1.0        # tie-breaker only
best_val_episode = None       # training episode at which the best ckpt was saved

for episode in range(1, NUM_EPISODES + 1):
    # A fixed per-episode seed gives every experiment the same initial-state
    # schedule without using validation, benchmark, or final-holdout seeds.
    state = env.reset(seed=TRAIN_ENV_SEED_BASE + episode - 1)
    total_reward = 0
    done = False

    while not done:
        action = agent.act(state)  # Agent selects an action using epsilon-greedy
        next_state, reward, done = env.step(action)  # Environment responds
        agent.step(state, action, reward, next_state, done)  # Agent learns from the experience
        state = next_state
        total_reward += reward

    episode_rewards.append(total_reward)

    # Decay epsilon once per episode (not per gradient step) to keep exploration
    # meaningful across the whole training run.
    agent.decay_epsilon()

    # Evaluate average max Q-value on hold-out states periodically to track stability
    if episode % Q_EVAL_EVERY == 0:
        with torch.no_grad():
            q_values = agent.policy_net(hold_out_states_tensor)
            max_q_values = q_values.max(dim=1)[0]
            average_q_value = max_q_values.mean().item()
            average_q_values.append(average_q_value)
            average_q_episodes.append(episode)

        print(f"Episode {episode}, Total Reward: {total_reward:.2f}, "
              f"Average Max Q-Value: {average_q_value:.4f}, Epsilon: {agent.epsilon:.4f}")

    # Periodic greedy validation checkpoint selection. Checkpoint on the
    # validation mean reward, using solved rate only as a tie-breaker so that
    # two near-equal means prefer the more reliable (higher solved-rate) policy.
    if episode % VALIDATE_EVERY == 0:
        val = run_greedy_validation(
            agent=agent,
            episodes=VALIDATION_EPISODES,
            base_seed=VALIDATION_BASE_SEED,
        )
        val["episode"] = episode
        validation_history.append(val)
        is_best = (val["mean_reward"] > best_val_mean) or (
            val["mean_reward"] == best_val_mean
            and val["solved_rate"] > best_val_solved
        )
        if is_best:
            best_val_mean = val["mean_reward"]
            best_val_solved = val["solved_rate"]
            best_val_episode = episode
            torch.save(agent.policy_net.state_dict(), WEIGHTS_PATH)
        print(f"[Validation @ ep {episode}] mean={val['mean_reward']:.2f} "
              f"median={val['median_reward']:.2f} std={val['std_reward']:.2f} "
              f"solved={val['solved_rate']*100:.0f}%"
              f"{'  <- NEW BEST (saved)' if is_best else ''}")

# --- Compute final training statistics ---
episode_rewards = np.asarray(episode_rewards, dtype=float)
rewards_ma = moving_average(episode_rewards, MOVING_AVG_WINDOW)
total_tests = int(len(episode_rewards))
mean_reward = float(np.mean(episode_rewards))
variance_reward = float(np.var(episode_rewards))

print("==============================")
print("Training Phase Completed!")
print(f"Total Episodes (Tests): {total_tests}")
print(f"Mean Reward: {mean_reward:.2f}")
print(f"Reward Variance: {variance_reward:.2f}")
print(f"Final Moving-Avg Reward (w={MOVING_AVG_WINDOW}): {rewards_ma[-1]:.2f}")
print(f"Final Epsilon: {agent.epsilon:.4f}")
print("==============================")

# --- Persist metrics for later analysis / report ---
metrics = {
    "seed": SEED,
    "num_episodes": total_tests,
    "hyperparameters": {
        "algorithm": ALGORITHM,
        "learning_rate": LEARNING_RATE,
        "target_update_freq": TARGET_UPDATE_FREQ,
        "target_update_unit": "learning_optimizer_updates",
        "replay_buffer_capacity": REPLAY_BUFFER_CAPACITY,
        "batch_size": BATCH_SIZE,
        "gamma": GAMMA,
        "epsilon_start": EPSILON_START,
        "epsilon_min": EPSILON_MIN,
        "epsilon_decay": EPSILON_DECAY,
        "epsilon_decay_unit": "episode",
        "num_episodes": NUM_EPISODES,
    },
    "reproducibility": {
        "global_seed": SEED,
        "python_random_seed": SEED,
        "numpy_seed": SEED,
        "torch_seed": SEED,
        "training_env_seed_scheme": "TRAIN_ENV_SEED_BASE + episode - 1",
        "training_env_seed_base": TRAIN_ENV_SEED_BASE,
        "training_env_seed_last": TRAIN_ENV_SEED_BASE + NUM_EPISODES - 1,
        "training_action_space_seed": TRAIN_ACTION_SPACE_SEED,
        "holdout_uses_separate_environment": True,
        "holdout_state_count": HOLDOUT_STATE_COUNT,
        "holdout_env_seed_base": HOLDOUT_ENV_SEED_BASE,
        "holdout_env_seed_last": HOLDOUT_ENV_SEED_BASE + hold_out_reset_count,
        "holdout_action_space_seed": HOLDOUT_ACTION_SPACE_SEED,
        "reserved_evaluation_seed_ranges": {
            "validation": [901, 910],
            "benchmark_a": [1234, 1283],
            "benchmark_b": [5000, 5099],
            "final_holdout": [10000, 10099],
        },
    },
    "moving_avg_window": MOVING_AVG_WINDOW,
    "q_eval_every": Q_EVAL_EVERY,
    "mean_reward": mean_reward,
    "variance_reward": variance_reward,
    "final_moving_avg_reward": float(rewards_ma[-1]),
    "final_epsilon": float(agent.epsilon),
    "episodes": list(range(1, total_tests + 1)),
    "episode_rewards": episode_rewards.tolist(),
    "moving_average_rewards": rewards_ma.tolist(),
    "q_eval_episodes": average_q_episodes,
    "average_q_values": average_q_values,
    "validation": {
        "config": {
            "validate_every": VALIDATE_EVERY,
            "episodes": VALIDATION_EPISODES,
            "base_seed": VALIDATION_BASE_SEED,
            "solved_threshold": SOLVED_THRESHOLD,
        },
        "best_val_mean_reward": None if best_val_mean == -float('inf') else best_val_mean,
        "best_val_solved_rate": None if best_val_episode is None else best_val_solved,
        "best_val_episode": best_val_episode,
        "history": validation_history,
    },
}
with open(METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=2)
print(f"Training metrics saved to {METRICS_PATH}.")

# --- Save non-interactive plots ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: total reward + moving average (+ validation mean on a twin axis)
ep_idx = np.arange(1, total_tests + 1)
axes[0].plot(ep_idx, episode_rewards, color="lightgray", label="Episode reward")
axes[0].plot(ep_idx, rewards_ma, color="blue", linewidth=2,
             label=f"Moving avg (w={MOVING_AVG_WINDOW})")
axes[0].set_title("Episode Reward & Moving Average")
axes[0].set_xlabel("Episode")
axes[0].set_ylabel("Reward")
axes[0].grid(True, alpha=0.3)

# Validation mean reward (greedy, deployment-quality criterion) on a twin axis.
# Plotted as sparse markers so it does not clutter the dense reward curve.
if validation_history:
    val_eps = [v["episode"] for v in validation_history]
    val_means = [v["mean_reward"] for v in validation_history]
    ax_val = axes[0].twinx()
    ax_val.plot(val_eps, val_means, color="red", marker="D", markersize=4,
                linestyle="--", linewidth=1.2, label="Greedy val mean")
    ax_val.set_ylabel("Greedy validation mean", color="red")
    ax_val.tick_params(axis="y", labelcolor="red")
    # Merge legends from both axes into the left panel's legend.
    h1, l1 = axes[0].get_legend_handles_labels()
    h2, l2 = ax_val.get_legend_handles_labels()
    axes[0].legend(h1 + h2, l1 + l2, loc="lower right")
else:
    axes[0].legend()

# Right (optional): average max Q over hold-out states, if collected
if average_q_values:
    axes[1].plot(average_q_episodes, average_q_values, color="green", marker="o", markersize=3)
    axes[1].set_title("Average Max Q-Value (Hold-out States)")
    axes[1].set_xlabel("Episode")
    axes[1].set_ylabel("Average Max Q")
    axes[1].grid(True, alpha=0.3)
else:
    axes[1].set_visible(False)

fig.tight_layout()
fig.savefig(PLOT_PATH, dpi=120)
plt.close(fig)
print(f"Training plot saved to {PLOT_PATH}.")

# --- Correct environment cleanup ---
env.close()
