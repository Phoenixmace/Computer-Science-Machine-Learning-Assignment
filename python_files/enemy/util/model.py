import torch
from torch import nn as nn
import os

class deeplearning_model(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_size)
        )

    def forward(self, x):
        return self.net(x)

    def get_action_from_model(self, state):
        state_tensor = torch.tensor(state, dtype=torch.float32)
        state_tensor = state_tensor / 500.0
        state_tensor = state_tensor.unsqueeze(0)

        with torch.no_grad():
            q_values = self(state_tensor)

        action = torch.argmax(q_values).item()
        return action
    def save_model(self, enemy_type="untitled", level=0,number=0):
        path = os.path.join(os.getcwd().split("python_files")[0], "assets", "models", f"{enemy_type}_{level}_{number}.pt")
        torch.save(self.state_dict(), path)
        print("Model saved.")
    def load_model(self, enemy_type="untitled", level=0, number=0):
        path = os.path.join(os.getcwd().split("python_files")[0], "assets", "models", f"{enemy_type}_{level}_{number}.pt")
        self.load_state_dict(torch.load(path))
        self.eval()
        print("Model loaded.")