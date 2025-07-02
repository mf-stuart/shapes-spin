import numpy as np

from typing_extensions import override


from tools import normpify_3vector, numpify_3vector
from vectorshape.shape import Shape
from vectorshape.vertice import Vertice

class Polygon(Shape):
    def __init__(self, pos_arr: tuple[float, float, float], name: str):
        super().__init__(pos_arr, name)
        self.normal: np.array = None
        self.vertices_loop: list[Vertice] = []

    def get_vertices(self) -> list[Vertice]:
        return self.vertices_loop

    def add_vertice(self, vertice: Vertice):
        if vertice not in self.vertices_loop and self.new_vertex_fits(vertice):
            self.vertices_loop.append(vertice)

    def remove_vertice(self, vertice: Vertice):
        self.vertices_loop.remove(vertice)
        if len(self.vertices_loop) < 3:
            self.normal = None

    def generate_plane(self) -> tuple[float, float, float, float]:
        if len(self.vertices_loop) < 3:
            raise TypeError("FlatShape does not have enough vertices to generate a plane.")

        self.calibrate_center()

        p = self.pos
        px = p[0]
        py = p[1]
        pz = p[2]

        v1 = self.vertices_loop[0] - p
        v2 = self.vertices_loop[1] - p

        self.normal = normpify_3vector(np.cross(v1, v2))


        a, b, c = self.normal
        d = -(a*px + b*py + c*pz)
        return a, b, c, d

    def ensure_normal_out(self, solid: Shape):
        to_face = self.vertices_loop[0].get_pos() - solid.get_pos()
        if np.dot(to_face, self.normal) < 0:
            self.normal = -self.normal

    def get_normal(self) -> np.ndarray:
        return self.normal

    def new_vertex_fits(self, vertice: Vertice):
        if self.normal is None:
            return True
        return np.dot(vertice.get_pos() - self.pos, self.normal) == 0

    @override
    def calibrate_center(self):
        self.pos = np.mean([vertice.get_pos() for vertice in self.vertices_loop], axis=0)

    @override
    def shift_position(self, movement_vec: tuple[float, float, float]):
        movement_vec = numpify_3vector(movement_vec)

    @override
    def rotate(self, angle: tuple[float, float, float]):
        pass

