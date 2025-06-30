import numpy as np


class Vertice:
    def __init__(self, pos_arr: tuple[float, float, float]):
        self.pos: np.array = np.array(pos_arr)
        self.friends = []

    def get_pos(self) -> np.ndarray:
        return self.pos

