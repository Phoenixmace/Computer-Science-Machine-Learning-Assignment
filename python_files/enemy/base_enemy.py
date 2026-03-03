from asyncio import exceptions

from python_files.enemy.util.model import deeplearning_model
from python_files.godot_util.godot_util import *
import os
import json

class BaseEnemy:
    def __init__(self, level, type, number=0, state_size=8, action_size=9):
        self.level = level
        self.type = type
        self.number = number
        self.model = self.load_model(state_size, action_size)

        self.current_session_data = {"steps":[]}
    def load_model(self, state_size, action_size):
        try:
            model = deeplearning_model(state_size, action_size)
            model.load_model(self.type, self.level)
            return model
        except Exception as e:
            print("Model not found, creating new model")
            print(e)
            return deeplearning_model(state_size, action_size, is_usable=False)

    def create_new_data_step(self):
        pass
    def get_action_and_add_data_sample(self):
        pass
    def get_object_hash(self):
        return f"{self.type}_{self.level}_{self.number}"

    def update_dataset_and_model(self):
        pass