from python_files.enemy.util.model import deeplearning_model
from python_files.godot_util.godot_util import *

class BaseEnemy:
    def __init__(self, level, type, state_size=8, action_size=9):
        self.level = level
        self.type = type
        self.model = deeplearning_model(state_size, action_size)
        self.current_session_data = {"steps":[]}
    def load_model(self, state_size, action_size):
        try:
            deeplearning_model(state_size, action_size)
            return deeplearning_model.load_model(self.type, self.level)
        except:
            print("Model not found")
            return False

    def get_data_sample(self):
        pass
    def get_action_and_add_data_sample(self):
        pass