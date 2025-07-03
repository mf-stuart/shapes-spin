from tools import numpify_3vector
import numpy as np

class Vertice:
    def __init__(self, pos_arr: tuple[float, float, float], name: str):
        self.pos: np.ndarray = numpify_3vector(pos_arr)
        self.name: str = name

    def __repr__(self):
        return f'<Vertice "{self.name}": [{self.pos[0]},{self.pos[1]},{self.pos[2]}]>'

    def set_pos(self, pos_arr: tuple[float, float, float]):
        self.pos = numpify_3vector(pos_arr)

    def get_pos(self) -> np.ndarray:
        return self.pos

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name
