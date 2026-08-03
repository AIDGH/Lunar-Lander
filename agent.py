import random
import torch
import torch.optim as optim
from model import DQN
import numpy as np

class ReplayBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.position = 0

    def push(self, state, action, reward, next_state, done):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)

class Agent:
    def __init__(self,
                 action_size,
                 state_size,
                 batch_size,
                 replay_buffer_capacity=10000,
                 gamma=0.99,
                 epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995,
                 lr=1e-3,
                 target_update_freq=1000,
                 tau=0.005):
        
        # Core hyperparameters
        self.action_size = action_size
        self.state_size = state_size
        self.batch_size = batch_size
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.lr = lr
        # Retained only for constructor compatibility with the base branch.
        # Soft updates are applied after every successful optimizer step.
        self.target_update_freq = target_update_freq
        if not 0.0 < tau <= 1.0:
            raise ValueError("tau must be in the interval (0, 1].")
        self.tau = tau

        # Initialize experience replay memory
        self.replay_buffer = ReplayBuffer(replay_buffer_capacity)
        
        # Initialize Policy and Target Networks
        self.policy_net = DQN(state_size, action_size)
        self.target_net = DQN(state_size, action_size)
        
        # Copy initial weights from Policy Net to Target Net
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
        # Set target network to evaluation mode (no gradients needed)
        self.target_net.eval()
        
        # Setup the optimizer for the Policy Network
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.lr)

    def act(self, state):
        # Epsilon-greedy action selection to balance exploration and exploitation
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        else:
            with torch.no_grad():
                # Convert state to tensor and add batch dimension
                state_tensor = torch.FloatTensor(state).unsqueeze(0)  
                q_values = self.policy_net(state_tensor)
                return q_values.argmax().item()

    def step(self, state, action, reward, next_state, done):
        # Store the experience in the replay buffer
        self.replay_buffer.push(state, action, reward, next_state, done)
        
        # Trigger the learning process if enough samples are available in memory
        if len(self.replay_buffer) >= self.batch_size:
            self.learn()

    def learn(self):
        # Sample a batch of experiences from the replay buffer
        batch = self.replay_buffer.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        # Convert to tensors for PyTorch operations
        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(np.array(actions)).unsqueeze(1)  # Add dimension for gather
        rewards = torch.FloatTensor(np.array(rewards)).unsqueeze(1)
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.FloatTensor(np.array(dones)).unsqueeze(1)

        # Compute Q-values for current states using the policy network
        current_q_values = self.policy_net(states).gather(1, actions)

        # Compute Q-values for next states using the target network
        with torch.no_grad():
            max_next_q_values = self.target_net(next_states).max(1)[0].unsqueeze(1)
            target_q_values = rewards + (self.gamma * max_next_q_values * (1 - dones))

        # Compute the loss between current and target Q-values.
        # Huber (Smooth L1) loss is more robust to large Q-value errors than MSE.
        loss = torch.nn.functional.smooth_l1_loss(current_q_values, target_q_values)

        # Optimize the policy network
        self.optimizer.zero_grad()
        loss.backward()
        # Clip gradients to stabilise training against occasional large updates
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), max_norm=1.0)
        self.optimizer.step()

        # Soft-update the target network after every successful optimizer step.
        with torch.no_grad():
            for target_param, policy_param in zip(
                    self.target_net.parameters(),
                    self.policy_net.parameters()):
                target_param.mul_(1.0 - self.tau)
                target_param.add_(policy_param, alpha=self.tau)

    def decay_epsilon(self):
        # Decay epsilon once per episode (not per gradient step) so exploration
        # remains meaningful across the full training run instead of collapsing
        # within the first few episodes.
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)