import torch
import time
from game import LunarLanderEnv
from agent import Agent

# Initialize the environment with graphical rendering enabled
env = LunarLanderEnv(render_mode="human")
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

# Initialize the agent (hyperparameters like batch_size don't matter here)
agent = Agent(action_size=action_size, 
              state_size=state_size, 
              batch_size=64)

# Load the best trained weights
agent.policy_net.load_state_dict(torch.load('weights.pth'))
agent.policy_net.eval()  # Set network to evaluation mode (disables dropout/batchnorm if any)

# Force the agent to strictly exploit the learned policy (turn off random exploration)
agent.epsilon = 0.0

print("Starting evaluation...")

for episode in range(1, 6):  # Test for 5 episodes
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.act(state)  # Agent selects the best action based on policy_net
        next_state, reward, done = env.step(action)
        state = next_state
        total_reward += reward
        
        # Add a tiny sleep to make the graphical rendering easier to watch
        time.sleep(0.02)

    print(f"Test Episode {episode}: Total Reward = {total_reward:.2f}")

env.close()