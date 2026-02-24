from python_files.enemy.base_enemy import BaseEnemy
from python_files.godot_util.godot_util import *

class MeleeEnemy(BaseEnemy):
    def __init__(self, level, type, state_size=8, action_size=9):
        super().__init__(level, type, state_size, action_size)

    def get_data_sample(self, enemy_position, player_position, player_vector, enemy_vector, input_x=0, input_y=0):
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

        action = action_map.get((input_x, input_y), 8)
        step = {
            "enemy_pos_x": enemy_position[0],
            "enemy_pos_y": enemy_position[1],
            "player_pos_x": player_position[0],
            "player_pos_y": player_position[1],
            "enemy_vel_x": enemy_vector[0],
            "enemy_vel_y": enemy_vector[1],
            "player_vel_x": player_vector[0],
            "player_vel_y": player_vector[1],
            "action": action
        }
        return step
    def get_action_and_add_data_sample(self, observations):
        enemy_position = convert_godot_tuple_to_python_list(observations.get("global_position", ""))
        player_position = convert_godot_tuple_to_python_list(observations.get("player_relative", ""))
        player_vector = convert_godot_tuple_to_python_list(observations.get("player_vector", ""))
        enemy_vector = convert_godot_tuple_to_python_list(observations.get("enemy_vector", ""))