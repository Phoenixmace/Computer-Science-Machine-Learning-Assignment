import random
import os
import json
from python_files.enemy.util.model import deeplearning_model
import torch
global current_session_data
current_session_data = {"enemies":{}}
global enemy_model
model = deeplearning_model(state_size=8, action_size=9)
enemy_model = model.load_state_dict(torch.load(os.path.join(os.getcwd().split("python_files")[0], "assets", "models", "model.pt")))

from python_files.enemy.melee_enemy.melee_enemy import MeleeEnemy
enemy_classes = {"melee":MeleeEnemy}




def load_training_data(path=os.path.join(os.getcwd().split("python_files")[0], "assets", "training_data", "poc_data.json")):
    with open(path, "r") as f:
        return json.load(f)
def random_policy():
    return {"x": random.randint(-1, 1), "y": random.randint(-1, 1)}
def model_policy(step):
    global model
    state = [val for val in step.values()][:-1]
    print(state, step)
    model = deeplearning_model(state_size=8, action_size=9)
    action = model.get_action_from_model(state)
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
    print(action)
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
    # get enemy object
    level = args.get("level_name", "dev")
    enemy_type = args.get("type", "melee")
    enemy_number = args.get("number", str(0))
    enemy_name = f"{enemy_type}_{level}_{enemy_number}"
    if enemy_name in current_session_data["enemies"]:
        enemy_object = current_session_data["enemies"][enemy_name]
    else:
        enemy_object = enemy_classes[enemy_type](level=level,type=enemy_type,number=enemy_number)
        enemy_object_hash = enemy_object.get_object_hash()
        current_session_data["enemies"][enemy_object_hash] = enemy_object



    # Parse observations
    observations = args.get("observation", [])
    previous_reward = args.get("previous_reward", None)


    return_value = enemy_object.get_action_and_add_data_sample(observations, previous_reward)

    return return_value
async def close_session(args):
    print("close_session")
    global current_session_data
    for enemy in current_session_data["enemies"].values():
        enemy.update_dataset_and_model()
    return {"message": "Session closed"}
