import numpy as np


class Vertice:
    def __init__(self, pos_arr: list[float]):
        self.pos = np.array(pos_arr)
        self.friends = []

