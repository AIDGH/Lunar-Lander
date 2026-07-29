import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()

        # Define the architecture of the neural network
        self.fc1 = nn.Linear(state_size, 128)  # First fully connected layer
        self.fc2 = nn.Linear(128, 128)         # Second fully connected layer
        self.value_head = nn.Linear(128, 1)
        self.advantage_head = nn.Linear(128, action_size)

    def forward(self, x):
        # Forward pass through the network with ReLU activations
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        
        value = self.value_head(x)
        advantage = self.advantage_head(x)

        return value + advantage - advantage.mean(dim=1, keepdim=True)
