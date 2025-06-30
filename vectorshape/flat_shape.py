import numpy as np
from vectorshape.shape import Shape

class FlatShape(Shape):
    def __init__(self, pos_arr: tuple[float, float, float], normal_arr: tuple[float, float, float]):
        super().__init__(pos_arr)
        self.normal: np.array = np.array(normal_arr)