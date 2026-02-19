import random
import os
import json
from python_files.enemy_ai.proof_of_concept.convert_dataset import DQN, get_action_from_model
import torch
global current_session_data
current_session_data = {"steps":[]}
global enemy_model
model = DQN(state_size=8, action_size=9)
enemy_model = model.load_state_dict(torch.load(os.path.join(os.getcwd().split("python_files")[0], "assets", "models", "model.pt")))

def load_training_data(path=os.path.join(os.getcwd().split("python_files")[0], "assets", "training_data", "poc_data.json")):
    with open(path, "r") as f:
        return json.load(f)
def random_policy():
    return {"x": random.randint(-1, 1), "y": random.randint(-1, 1)}
def model_policy(step):
    global model
    state = [val for val in step.values()][:-1]
    action = get_action_from_model(state, model)
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
        if value == action:
            return {"x": key[0], "y": key[1]}
def get_data_sample(enemy_position, player_position, player_vector, enemy_vector, input_x=0, input_y=0):
  # idle
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

    action =  action_map.get((input_x, input_y ), 8)
    step= {
        "enemy_pos_x": enemy_position[0],
        "enemy_pos_y": enemy_position[1],
        "player_pos_x": player_position[0],
        "player_pos_y":player_position[1],
        "enemy_vel_x": enemy_vector[0],
        "enemy_vel_y": enemy_vector[1],
        "player_vel_x": player_vector[0],
        "player_vel_y": player_vector[1],
        "action":action
    }
    return step


def convert_godot_tuple_to_python_list(tuple):
    tuple = [float(i) for i in tuple.strip("()").split(", ")]
    return tuple
async def poc_enemy_movement(args):
    global current_session_data
    observations = args.get("observation", [])
    enemy_position = convert_godot_tuple_to_python_list(observations.get("global_position", ""))
    player_position = convert_godot_tuple_to_python_list(observations.get("player_relative", ""))
    player_vector = convert_godot_tuple_to_python_list(observations.get("player_vector", ""))
    enemy_vector = convert_godot_tuple_to_python_list(observations.get("enemy_vector", ""))
    previous_reward = args.get("previous_reward", None)
    return_value = random_policy()
    input_x = return_value.get("x", 0)
    input_y = return_value.get("y", 0)
    step = get_data_sample(enemy_position, player_position, player_vector, enemy_vector, input_x, input_y)
    if previous_reward and len(current_session_data["steps"]) > 0:
        current_session_data["steps"][-1]["reward"] = previous_reward
    current_session_data["steps"].append(step)

    if len(current_session_data["steps"]) <3:
        print(current_session_data["steps"])
    return model_policy(step)
async def close_session(args):
    print("close_session")
    global current_session_data
    training_data = load_training_data()
    training_data[str(len(training_data)+1)] = current_session_data
    json.dump(training_data, open(os.path.join(os.getcwd().split("python_files")[0], "assets","training_data", "poc_data.json"), "w"), indent=4)
    current_session_data = {"steps": []}
    return {"message": "Session closed successfully"}