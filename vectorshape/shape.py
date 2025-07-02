import numpy as np
from tools import numpify_3vector, normpify_3vector
from typing import Tuple

class Shape:
    def __init__(self, pos_arr: Tuple[float, float, float], name: str):
        if len(pos_arr) != 3:
            raise ValueError("Coordinate vectors take exactly 3 dimensions")
        self.pos: np.ndarray = numpify_3vector(pos_arr)
        self.name = name

    def get_pos(self) -> np.ndarray:
        return self.pos

    def set_pos(self, pos_arr: Tuple[float]):
        if len(pos_arr) != 3:
            raise ValueError("Coordinate vectors take exactly 3 dimensions")
        self.pos = numpify_3vector(pos_arr)

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def calibrate_center(self):
        raise NotImplementedError(f"{self.__class__.__name__} does not implement calibrate_center")

    def shift_position(self, movement_vec: tuple[float, float, float]):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement shift_position')

    def rotate(self, angle: tuple[float, float, float]):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement rotate')
