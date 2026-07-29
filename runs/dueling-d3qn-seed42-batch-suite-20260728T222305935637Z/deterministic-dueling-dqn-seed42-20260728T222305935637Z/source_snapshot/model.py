import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()

        # Define the architecture of the neural network
        self.fc1 = nn.Linear(state_size, 128)  # First fully connected layer
        self.fc2 = nn.Linear(128, 128)         # Second fully connected layer
        self.fc3 = nn.Linear(128, action_size) # Output layer for Q-values

    def forward(self, x):
        # Forward pass through the network with ReLU activations
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        
        return self.fc3(x)  # Output Q-values for each action


class DuelingDQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DuelingDQN, self).__init__()

        # Shared feature layers, identical in shape and construction order to
        # the standard DQN.
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)

        # Construct the advantage head before the additional value head so the
        # shared layers and four-output head consume the same initial random
        # draws as fc1, fc2, and fc3 in the standard DQN.
        self.advantage_head = nn.Linear(128, action_size)
        self.value_head = nn.Linear(128, 1)

    def forward(self, x):
        # x: [B, state_size] -> shared features: [B, 128]
        x = F.relu(self.fc1(x))
        features = F.relu(self.fc2(x))

        # value: [B, 1], advantage: [B, action_size]
        value = self.value_head(features)
        advantage = self.advantage_head(features)

        # Keep the action mean as [B, 1] for safe broadcasting, including
        # batch size one. The result is [B, action_size].
        return value + advantage - advantage.mean(dim=-1, keepdim=True)
