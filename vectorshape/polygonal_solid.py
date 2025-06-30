import numpy as np
from vectorshape.shape import Shape


class PolygonalSolid(Shape):
    def __init__(self, pos_arr: tuple[float, float, float]):
        super().__init__(pos_arr)
        self.faces = []
