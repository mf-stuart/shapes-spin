from typing_extensions import override

import numpy as np
from tools import numpify_3vector, normpify_3vector
from vectorshape.polygon import Polygon
from vectorshape.shape import Shape
from vectorshape.vertice import Vertice


class PolygonalSolid(Shape):
    def __init__(self, pos_arr: tuple[float, float, float], this_way_up_arr: tuple[float, float, float], name: str):
        super().__init__(pos_arr, name)
        self.this_way_up = normpify_3vector(this_way_up_arr)
        self.faces: list[Polygon] = []

    @override
    def calibrate_center(self):
        vertices: list[Vertice] = []
        for face in self.faces:
            for vertex in face.get_vertices():
                if vertex not in vertices:
                    vertices.append(vertex)
        self.pos = np.mean([vertice.get_pos() for vertice in vertices], axis=0)

    @override
    def shift_position(self, movement_vec: tuple[float, float, float]):
        movement_vec = numpify_3vector(movement_vec)
        self.pos += movement_vec
        for face in self.faces:
            face.shift_position(movement_vec)

    @override
    def rotate(self, matrix: np.array, pivot_vec: tuple[float, float, float]):
        pivot_vec = numpify_3vector(pivot_vec)
        pass
