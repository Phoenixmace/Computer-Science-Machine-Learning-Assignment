import json
import torch
import numpy as np
import os

with open(os.path.join(os.getcwd().split("python_files")[0], "assets", "training_data", "poc_data.json")) as f:
    data = json.load(f)

states = []
actions = []
rewards = []
next_states = []

for episode in data.values():
    steps = episode["steps"]

    for i in range(len(steps) - 4):
        s = steps[i+1]
        s_next = steps[i + 2]

        if "reward" not in s:
            continue

        state_vec = [
            s["enemy_pos_x"],
            s["enemy_pos_y"],
            s["player_pos_x"],
            s["player_pos_y"],
            s["enemy_vel_x"],
            s["enemy_vel_y"],
            s["player_vel_x"],
            s["player_vel_y"]
        ]

        next_state_vec = [
            s_next["enemy_pos_x"],
            s_next["enemy_pos_y"],
            s_next["player_pos_x"],
            s_next["player_pos_y"],
            s_next["enemy_vel_x"],
            s_next["enemy_vel_y"],
            s_next["player_vel_x"],
            s_next["player_vel_y"]
        ]
        states.append(state_vec)
        next_states.append(next_state_vec)
        rewards.append(s["reward"])
        actions.append(s["action"])
states = torch.tensor(states, dtype=torch.float32)
next_states = torch.tensor(next_states, dtype=torch.float32)
actions = torch.tensor(actions, dtype=torch.long)
rewards = torch.tensor(rewards, dtype=torch.float32)

import torch.nn as nn

class DQN(nn.Module):
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
def save_model(model, path=os.path.join(os.getcwd().split("python_files")[0], "assets", "models", "model.pt")):
    torch.save(model.state_dict(), path)
    print("Model saved.")
model = DQN(state_size=8, action_size=9)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()
gamma = 0.99
q_values = model(states)
print("q_values shape:", q_values.shape)
print("actions shape:", actions.shape)
q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze()

with torch.no_grad():
    next_q_values = model(next_states)
    max_next_q = next_q_values.max(1)[0]
    target = rewards + gamma * max_next_q

loss = criterion(q_value, target)

optimizer.zero_grad()
loss.backward()
optimizer.step()
save_model(model)


def get_action_from_model(state, model):
    state_tensor = torch.tensor(state, dtype=torch.float32)

    # Normalize (important)
    state_tensor = state_tensor / 500.0

    state_tensor = state_tensor.unsqueeze(0)  # add batch dimension

    with torch.no_grad():
        q_values = model(state_tensor)

    action = torch.argmax(q_values).item()

    return action