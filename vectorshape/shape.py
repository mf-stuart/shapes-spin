import numpy as np
from tools import numpify_3vector

class Shape:
    def __init__(self, pos_arr: tuple[float, float, float], name: str):
        self.pos: np.ndarray = numpify_3vector(pos_arr)
        self.name = name

    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.name}": at [{self.pos[0]},{self.pos[1]},{self.pos[2]}]>'

    def get_pos(self) -> np.ndarray:
        return self.pos

    def set_pos(self, pos_arr: tuple[float, float, float]):
        self.pos = numpify_3vector(pos_arr)

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def calibrate_center(self):
        raise NotImplementedError(f"{self.__class__.__name__} does not implement calibrate_center")

    def shift_position(self, movement_vec: tuple[float, float, float]):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement shift_position')

    def rotate(self, matrices: list[np.ndarray], pivot_vec: tuple[float, float, float]):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement rotate')
