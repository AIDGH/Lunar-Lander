import numpy as np
import torch
from game import LunarLanderEnv
from agent import Agent

# Initialize the environment
env = LunarLanderEnv()
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

# Initialize the agent with standard hyperparameters
agent = Agent(action_size=action_size, 
              state_size=state_size, 
              batch_size=64)

# --- Hold-out States Collection ---
# Collect a set of random states to track Q-value stability during training
hold_out_states = []
state = env.reset()

for _ in range(200):
    action = env.action_space.sample()  # Take a random action
    next_state, reward, done = env.step(action)
    hold_out_states.append(state)
    state = next_state
    if done:
        state = env.reset()

# Convert hold-out states to tensor for fast evaluation later
hold_out_states_tensor = torch.FloatTensor(np.array(hold_out_states))

# Lists to keep track of rewards and average max Q-values for reporting
episode_rewards = []
average_q_values = []

# Initialize best reward tracker
best_reward = -float('inf')

for episode in range(1, 1001):  # Train for 1000 episodes
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.act(state)  # Agent selects an action using epsilon-greedy
        next_state, reward, done = env.step(action)  # Environment responds
        agent.step(state, action, reward, next_state, done)  # Agent learns from the experience
        state = next_state
        total_reward += reward

    episode_rewards.append(total_reward)

    # Evaluate average max Q-value on hold-out states every 10 episodes to track stability
    if episode % 10 == 0:
        with torch.no_grad():
            # Use policy_net instead of qnetwork_local
            q_values = agent.policy_net(hold_out_states_tensor)
            max_q_values = q_values.max(dim=1)[0]
            average_q_value = max_q_values.mean().item()
            average_q_values.append(average_q_value)

        print(f"Episode {episode}, Total Reward: {total_reward:.2f}, Average Max Q-Value: {average_q_value:.4f}")

    # Save the model weights if the current episode achieved the highest reward
    if total_reward > best_reward:
        best_reward = total_reward
        torch.save(agent.policy_net.state_dict(), 'weights.pth')
        print(f"New best reward: {best_reward:.2f}! Weights saved to weights.pth.")