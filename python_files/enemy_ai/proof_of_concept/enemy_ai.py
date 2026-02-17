import random
import os
import json
global current_session_data
current_session_data = {"steps":[]}
def load_training_data(path=os.path.join(os.getcwd().split("python_files")[0], "assets", "training_data", "poc_data.json")):
    with open(path, "r") as f:
        return json.load(f)
def random_policy():
    return {"x": random.randint(-1, 1), "y": random.randint(-1, 1)}

def get_data_sample(enemy_position, player_position, player_vector, enemy_vector):
    step= {
        "dx": enemy_position[0],
        "dy": enemy_position[1],
        "player_x": player_position[0],
        "player_y":player_position[1],
        "enemy_vel_x": enemy_vector[0],
        "enemy_vel_y": enemy_vector[1],
        "player_vel_x": player_vector[0],
        "player_vel_y": player_vector[1]
    }
    return step
async def poc_enemy_movement(args):
    global current_session_data
    observations = args.get("observation", [])
    enemy_position = observations.get("global_position", "")
    player_position = observations.get("player_relative", "")
    player_vector = observations.get("player_vector", "")
    enemy_vector = observations.get("enemy_vector", "")
    previous_reward = args.get("previous_reward", None)
    step = get_data_sample(enemy_position, player_position, player_vector, enemy_vector)
    current_session_data["steps"].append(step)
    if previous_reward:
        current_session_data["steps"][-1]["reward"] = previous_reward
    return random_policy()
async def close_session(args):
    print("close_session")
    global current_session_data
    training_data = load_training_data()
    training_data[str(len(training_data)+1)] = current_session_data
    json.dump(training_data, open(os.path.join(os.getcwd().split("python_files")[0], "assets","training_data", "poc_data.json"), "w"))
    current_session_data = {"steps": []}
    return {"message": "Session closed successfully"}