from python_files.enemy.base_enemy import BaseEnemy
from python_files.godot_util.godot_util import *
import os
import json

# get response and add data sample with action and
class MeleeEnemy(BaseEnemy):
    def __init__(self, level, type, number=0, state_size=8, action_size=9):
        super().__init__(level, type,number, state_size, action_size)

    def create_new_data_step(self, enemy_position, player_position, player_vector, enemy_vector):
        # idle
        step = {
            "enemy_pos_x": enemy_position[0],
            "enemy_pos_y": enemy_position[1],
            "player_pos_x": player_position[0],
            "player_pos_y": player_position[1],
            "enemy_vel_x": enemy_vector[0],
            "enemy_vel_y": enemy_vector[1],
            "player_vel_x": player_vector[0],
            "player_vel_y": player_vector[1],
        }
        return step
    def add_action_to_data_step(self, action):
        self.current_step["action"] = action
    def get_action_and_add_data_sample(self, observations, previous_reward=None):
        # Parse observations
        enemy_position = convert_godot_tuple_to_python_list(observations.get("global_position", ""))
        player_position = convert_godot_tuple_to_python_list(observations.get("player_relative", ""))
        player_vector = convert_godot_tuple_to_python_list(observations.get("player_vector", ""))
        enemy_vector = convert_godot_tuple_to_python_list(observations.get("enemy_vector", ""))
        if previous_reward and len(self.current_session_data["steps"]) > 0 and "previous_reward" not in self.current_session_data["steps"][-1]:
            self.current_session_data["steps"][-1]["previous_reward"] = previous_reward
        self.current_step = self.create_new_data_step(enemy_position,player_position,player_vector,enemy_vector)
        return_action = self.model.get_action_from_model([value for value in self.current_step.values()])
        self.add_action_to_data_step(return_action)
        action_map = {
            (-1, 0): 0,
            (1, 0): 1,
            (0, -1): 2,
            (0, 1): 3,
            (-1, -1): 4,
            (1, -1): 5,
            (-1, 1): 6,
            (1, 1): 7,
            (0, 0): 8
        }
        for key, value in action_map.items():
            if value == return_action:
                return {"x": key[0], "y": key[1]}



    def update_dataset_and_model(self):
        print("Updating dataset and model")
        dataset_name = f"{self.get_object_hash()}_s{self.model.states}_a{self.model.actions}.json"
        dataset_path = os.path.join(os.getcwd().split("python_files")[0], "assets", "training_data", f"{dataset_name}")
        unformatted_data = self.current_session_data["steps"]
        states = []
        actions = []
        rewards = []
        next_states = []

        for i in range(len(unformatted_data) - 4):
            s = unformatted_data[i + 1]
            s_next = unformatted_data[i + 2]

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
        if not len(states) == len(next_states) == len(actions) == len(rewards):
            print("Error: Data length mismatch")
            return


        if os.path.exists(dataset_path):
            with open(dataset_path, "r") as f:
                data = json.load(f)
                data["states"].append(states)
                data["actions"].append(actions)
                data["rewards"].append(rewards)
                data["next_states"].append(next_states)
                json.dump(data, open(dataset_path, "w"))
        else:
            data = {}
            data["states"] = states
            data["actions"] = actions
            data["rewards"] = rewards
            data["next_states"] = next_states
            json.dump(data, open(dataset_path, "w"))
        print(os.path.exists(dataset_path))
        print(dataset_path)
        self.model.update_and_save_model(dataset_name)