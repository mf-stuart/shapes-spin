import numpy as np

class Shape:
    def __init__(self, pos_arr: list[float]):
        self.pos = np.array(pos_arr)

    def get_pos(self):
        return self.pos

    def set_pos(self, pos_arr):
        self.pos = pos_arr

