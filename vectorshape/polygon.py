import numpy as np
from vectorshape.flat_shape import FlatShape


class Polygon(FlatShape):
    def __init__(self, pos_arr, normal_arr):
        super().__init__(pos_arr, normal_arr)
        self.vertices = []
        self.edges = []

    def attach(self):
        pass