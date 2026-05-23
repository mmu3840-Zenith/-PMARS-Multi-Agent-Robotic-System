import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def forward(self, x):
        return self.net(x)

class DQNAgent:
    def __init__(self, state_dim, action_dim):
        self.model = DQN(state_dim, action_dim)
        self.target = DQN(state_dim, action_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.gamma = 0.99

    def select_action(self, state):
        if random.random() < 0.1:
            return random.randint(0,1)
        with torch.no_grad():
            return torch.argmax(self.model(torch.tensor(state, dtype=torch.float32))).item()

    def train_step(self, batch):
        states, actions, rewards, next_states = batch

        q_vals = self.model(states).gather(1, actions)
        next_q = self.target(next_states).max(1)[0].detach()
        target = rewards + self.gamma * next_q

        loss = nn.MSELoss()(q_vals.squeeze(), target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
