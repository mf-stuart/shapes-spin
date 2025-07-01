import numpy as np

class Shape:
    def __init__(self, pos_arr: tuple[float, float, float]):
        self.pos: np.array = np.array(pos_arr)

    def get_pos(self) -> np.array:
        return self.pos

    def set_pos(self, pos_arr: np.array):
        self.pos = pos_arr

