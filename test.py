import argparse
import json
import time
import numpy as np
import torch
from game import LunarLanderEnv
from agent import Agent

WEIGHTS_PATH = "weights.pth"

# LunarLander-v2 discrete action mapping (environment-defined constants,
# NOT a hand-written control rule). Actions fire at full power.
ACTION_NAMES = {
    0: "no_op",
    1: "fire_left_orientation_engine",
    2: "fire_main_engine",
    3: "fire_right_orientation_engine",
}
SIDE_ENGINE_ACTIONS = (1, 3)

# LunarLander-v2 observation vector layout (environment-defined).
STATE_KEYS = [
    "x", "y", "vx", "vy",
    "angle", "angular_velocity",
    "left_leg_contact", "right_leg_contact",
]


def _load_greedy_agent(env):
    """Build an Agent matched to the env sizes, load weights.pth, and force
    greedy (epsilon=0) evaluation. Used by both evaluation modes."""
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = Agent(action_size=action_size,
                  state_size=state_size,
                  batch_size=64)
    agent.policy_net.load_state_dict(
        torch.load(WEIGHTS_PATH, map_location='cpu', weights_only=True)
    )
    agent.policy_net.eval()
    agent.epsilon = 0.0
    return agent


def run_rendered(episodes=1000, algorithm="vanilla"):
    """Default mode: render greedy evaluation, identical to the original
    test.py workflow."""
    env = LunarLanderEnv(render_mode="human")
    agent = _load_greedy_agent(env)

    print("Starting evaluation...")

    eval_rewards = []
    total_wins = 0
    for episode in range(1, episodes + 1):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = agent.act(state)  # greedy: epsilon == 0
            next_state, reward, done = env.step(action)
            state = next_state
            total_reward += reward
            # time.sleep(0.02)  # make rendering watchable
        if total_reward >= 200.0:
            total_wins += 1
        eval_rewards.append(total_reward)
        print(f"Test Episode {episode}: Total Reward = {total_reward:.2f}")

    print("==============================")
    print(f"Mean Evaluation Reward (over {len(eval_rewards)} episodes): "
          f"{np.mean(eval_rewards):.2f}")
    print(f"Standard Deviation of Reward: {np.std(eval_rewards):.2f}")
    print(f"Win rate: {total_wins}/{len(eval_rewards)} ({total_wins/len(eval_rewards)*100:.2f}%)")
    print("==============================")

    env.close()


def _longest_run(actions, target):
    best = cur = 0
    for a in actions:
        if a == target:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 0
    return best


def run_diagnostic(episodes, base_seed, output_path, long_streak_threshold,
                   solved_threshold=200.0, low_score_threshold=0.0):
    """Non-rendered greedy evaluation over reproducible seeds, collecting
    metrics to determine whether the side-engine behaviour is systematic."""
    env = LunarLanderEnv()  # non-rendered
    agent = _load_greedy_agent(env)

    per_episode = []
    all_rewards = []
    all_lengths = []
    agg_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    overall_side_steps = 0
    overall_total_steps = 0
    max_side_streak = {1: 0, 3: 0}

    print(f"Starting diagnostic evaluation: {episodes} episodes, "
          f"base seed {base_seed} (no rendering)...")

    for ep in range(1, episodes + 1):
        seed = base_seed + (ep - 1)
        state = env.reset(seed=seed)
        done = False
        total_reward = 0.0
        actions = []

        # Streak tracking state
        cur_streak_action = None
        cur_streak_len = 0
        cur_streak_start_state = None
        cur_streak_start_q = None
        cur_streak_start_step = -1
        suspicious = []
        suspicious_cap = 10

        def close_streak(action, length, start_state, start_q, start_step):
            """Record a long side-engine streak as a suspicious event."""
            if action in SIDE_ENGINE_ACTIONS and length >= long_streak_threshold:
                if len(suspicious) < suspicious_cap and start_q is not None:
                    q_sorted = sorted(start_q, reverse=True)
                    margin = q_sorted[0] - q_sorted[1] if len(q_sorted) >= 2 else 0.0
                    suspicious.append({
                        "step": start_step,
                        "action": int(action),
                        "action_name": ACTION_NAMES[action],
                        "streak_length": int(length),
                        "q_values_at_start": {
                            ACTION_NAMES[a]: float(start_q[a]) for a in range(4)
                        },
                        "top1_minus_top2_margin": round(float(margin), 4),
                        "state_at_start": {
                            STATE_KEYS[i]: float(start_state[i]) for i in range(len(STATE_KEYS))
                        },
                    })

        while not done:
            with torch.no_grad():
                state_t = torch.FloatTensor(state).unsqueeze(0)
                q_vec = agent.policy_net(state_t)[0]
                # Greedy selection identical to agent.act() at epsilon=0
                # (torch.argmax breaks ties toward the first/lowest index).
                action = int(q_vec.argmax().item())
                q_list = [float(v) for v in q_vec.tolist()]

            next_state, reward, done = env.step(action)
            total_reward += reward
            actions.append(action)

            # Streak bookkeeping
            if action == cur_streak_action:
                cur_streak_len += 1
            else:
                close_streak(cur_streak_action, cur_streak_len,
                             cur_streak_start_state, cur_streak_start_q,
                             cur_streak_start_step)
                cur_streak_action = action
                cur_streak_len = 1
                cur_streak_start_state = state
                cur_streak_start_q = q_list
                cur_streak_start_step = len(actions) - 1

            state = next_state

        # Close the final streak of the episode
        close_streak(cur_streak_action, cur_streak_len,
                     cur_streak_start_state, cur_streak_start_q,
                     cur_streak_start_step)

        n = len(actions)
        counts = {a: int(actions.count(a)) for a in range(4)}
        longest_per_action = {a: int(_longest_run(actions, a)) for a in range(4)}
        side_steps = int(sum(counts[a] for a in SIDE_ENGINE_ACTIONS))

        # Final-phase analysis: last 20% of steps (proportional, no altitude rule)
        final_start = int(n * 0.8)
        final_phase = actions[final_start:]
        side_in_final = sum(1 for a in final_phase if a in SIDE_ENGINE_ACTIONS)

        for a in SIDE_ENGINE_ACTIONS:
            if longest_per_action[a] > max_side_streak[a]:
                max_side_streak[a] = longest_per_action[a]
        for a in range(4):
            agg_counts[a] += counts[a]
        overall_side_steps += side_steps
        overall_total_steps += n

        # Terminal observation (post last step)
        final_state = {STATE_KEYS[i]: float(state[i]) for i in range(len(STATE_KEYS))}

        per_episode.append({
            "episode": ep,
            "seed": int(seed),
            "total_reward": round(float(total_reward), 4),
            "length": int(n),
            "action_counts": counts,
            "action_pct": {
                ACTION_NAMES[a]: round(100.0 * counts[a] / n, 2) if n else 0.0
                for a in range(4)
            },
            "longest_streak_per_action": {
                ACTION_NAMES[a]: longest_per_action[a] for a in range(4)
            },
            "side_engine_overall_pct": round(100.0 * side_steps / n, 2) if n else 0.0,
            "side_engine_final_phase_pct": (
                round(100.0 * side_in_final / len(final_phase), 2) if final_phase else 0.0
            ),
            "final_state": final_state,
            "suspicious_events": suspicious,
        })

        all_rewards.append(float(total_reward))
        all_lengths.append(int(n))

        solved_flag = "SOLVED" if total_reward >= solved_threshold else "    "
        low_flag = "LOW" if total_reward < low_score_threshold else "   "
        print(f"  Ep {ep:3d} [{solved_flag}][{low_flag}] "
              f"reward={total_reward:8.2f}  len={n:4d}  "
              f"streak(L,R)=({longest_per_action[1]},{longest_per_action[3]})")

    rewards = np.asarray(all_rewards, dtype=float)
    lengths = np.asarray(all_lengths, dtype=float)
    solved_count = int(np.sum(rewards >= solved_threshold))
    low_count = int(np.sum(rewards < low_score_threshold))

    report = {
        "config": {
            "weights": WEIGHTS_PATH,
            "episodes": int(episodes),
            "base_seed": int(base_seed),
            "long_streak_threshold": int(long_streak_threshold),
            "solved_threshold": float(solved_threshold),
            "low_score_threshold": float(low_score_threshold),
            "greedy_epsilon": 0.0,
        },
        "summary": {
            "mean_reward": round(float(np.mean(rewards)), 4) if len(rewards) else 0.0,
            "median_reward": round(float(np.median(rewards)), 4) if len(rewards) else 0.0,
            "std_reward": round(float(np.std(rewards)), 4) if len(rewards) else 0.0,
            "min_reward": round(float(np.min(rewards)), 4) if len(rewards) else 0.0,
            "max_reward": round(float(np.max(rewards)), 4) if len(rewards) else 0.0,
            "solved_count": solved_count,
            "solved_rate_pct": round(100.0 * solved_count / episodes, 2) if episodes else 0.0,
            "low_score_count": low_count,
            "low_score_rate_pct": round(100.0 * low_count / episodes, 2) if episodes else 0.0,
            "mean_length": round(float(np.mean(lengths)), 2) if len(lengths) else 0.0,
            "aggregate_action_counts": agg_counts,
            "aggregate_action_pct": {
                ACTION_NAMES[a]: round(100.0 * agg_counts[a] / overall_total_steps, 2)
                if overall_total_steps else 0.0
                for a in range(4)
            },
            "side_engine_overall_pct": (
                round(100.0 * overall_side_steps / overall_total_steps, 2)
                if overall_total_steps else 0.0
            ),
            "max_side_engine_streak": {
                ACTION_NAMES[1]: int(max_side_streak[1]),
                ACTION_NAMES[3]: int(max_side_streak[3]),
            },
        },
        "rewards": [round(float(r), 4) for r in rewards.tolist()],
        "per_episode": per_episode,
    }

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    s = report["summary"]
    print("==============================")
    print("Diagnostic Summary")
    print(f"  Mean reward   : {s['mean_reward']:.2f}   Median: {s['median_reward']:.2f}   "
          f"Std: {s['std_reward']:.2f}")
    print(f"  Min / Max     : {s['min_reward']:.2f} / {s['max_reward']:.2f}")
    print(f"  Solved (>=200): {s['solved_count']}/{episodes} "
          f"({s['solved_rate_pct']:.1f}%)")
    print(f"  Low (<0)      : {s['low_score_count']}/{episodes} "
          f"({s['low_score_rate_pct']:.1f}%)")
    print(f"  Mean length   : {s['mean_length']:.1f}")
    print(f"  Action %      : " + ", ".join(
        f"{ACTION_NAMES[a]}={s['aggregate_action_pct'][ACTION_NAMES[a]]:.1f}%"
        for a in range(4)
    ))
    print(f"  Max side streak: L={s['max_side_engine_streak'][ACTION_NAMES[1]]}, "
          f"R={s['max_side_engine_streak'][ACTION_NAMES[3]]}")
    print(f"  Report saved  : {output_path}")
    print("==============================")

    env.close()


def main():
    parser = argparse.ArgumentParser(
        description="LunarLander DQN evaluation. Default: rendered greedy test."
    )
    parser.add_argument(
        "--diagnostic", action="store_true",
        help="Run a larger non-rendered greedy evaluation and write a JSON report."
    )
    parser.add_argument(
        "--episodes", type=int, default=50,
        help="Diagnostic episodes (default 50). Ignored in rendered mode."
    )
    parser.add_argument(
        "--seed", type=int, default=1234,
        help="Base seed for diagnostic reproducibility (default 1234)."
    )
    parser.add_argument(
        "--output", type=str, default="diagnostic_report.json",
        help="Diagnostic JSON output path (default diagnostic_report.json)."
    )
    parser.add_argument(
        "--long-streak", type=int, default=20,
        help="Side-engine streak length considered suspicious (default 20)."
    )
    args = parser.parse_args()

    if args.diagnostic:
        run_diagnostic(
            episodes=args.episodes,
            base_seed=args.seed,
            output_path=args.output,
            long_streak_threshold=args.long_streak,
        )
    else:
        run_rendered()


if __name__ == "__main__":
    main()
