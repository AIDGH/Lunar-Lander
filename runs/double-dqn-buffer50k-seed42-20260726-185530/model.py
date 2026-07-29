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