import numpy as np
from vectorshape.shape import Shape

class FlatShape(Shape):
    def __init__(self, pos_arr: list[float], normal_arr: list[float]):
        super().__init__(pos_arr)
        self.normal = np.array(normal_arr)