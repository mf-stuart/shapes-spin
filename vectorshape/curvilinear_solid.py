import numpy as np
from vectorshape.shape import Shape


class CurvilinearSolid(Shape):
    def __init__(self, pos_arr):
        super().__init__(pos_arr)
