import torch
from torch import nn as nn
import os
import json

class deeplearning_model(nn.Module):
    def __init__(self, state_size, action_size, is_usable=True):
        super().__init__()
        self.is_usable = is_usable
        self.states = state_size
        self.actions = action_size

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
    def save_model(self, enemy_type="untitled", level=0, number=0,file_name=None):
        if not file_name:
            file_name = f"{enemy_type}_{level}_{number}_s{self.states}_a{self.actions}.pt"
        else:
            file_name = f"{file_name}_s{self.states}_a{self.actions}.pt"
        path = os.path.join(os.getcwd().split("python_files")[0], "assets", "models", file_name)

        torch.save(self.state_dict(), path)
        print("Model saved.")
    def load_model(self, enemy_type="untitled", level=0, number=0,file_name=None):
        if not file_name:
            file_name = f"{enemy_type}_{level}_{number}_s{self.states}_a{self.actions}.pt"
        else:
            file_name = f"{file_name}_s{self.states}_a{self.actions}.pt"
        path = os.path.join(os.getcwd().split("python_files")[0], "assets", "models", file_name)
        self.load_state_dict(torch.load(path))
        self.eval()
        print("Model loaded.")
    def update_and_save_model(self, dataset_name="dev_level"):
        dataset_path = os.path.join(os.getcwd().split("python_files")[0], "assets", "training_data", f"{dataset_name}")

        with open(dataset_path) as f:
            data = json.load(f)
        states = data.get("states", [])
        actions = data.get("actions", [])
        rewards = data.get("rewards", [])
        next_states = data.get("next_states", [])
        states = torch.tensor(states, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        criterion = nn.MSELoss()
        gamma = 0.99
        q_values = self(states)
        print("q_values shape:", q_values.shape)
        print("actions shape:", actions.shape)
        q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze()

        with torch.no_grad():
            next_q_values = self(next_states)
            max_next_q = next_q_values.max(1)[0]
            target = rewards + gamma * max_next_q

        loss = criterion(q_value, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print("Model updated.")
        self.save_model(file_name=dataset_name)