import json
import torch
import os
import torch.nn as nn
from python_files.enemy.util.model import deeplearning_model


def update_model(level_name="dev_level"):

    with open(os.path.join(os.getcwd().split("python_files")[0], "assets", "training_data", f"{level_name}.json")) as f:
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



    model = deeplearning_model(state_size=8, action_size=9)
    model.save()
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
    model.save()





