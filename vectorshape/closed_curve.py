import numpy as np
from vectorshape.flat_shape import FlatShape


class ClosedCurve(FlatShape):
    def __init__(self, pos_arr: tuple[float, float, float], normal_arr: tuple[float, float, float]):
        super().__init__(pos_arr, normal_arr)