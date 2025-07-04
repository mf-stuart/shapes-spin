import numpy as np
import default_constants as k

from typing import override

from tools import normpify_3vector
from vectorshape.polygon import Polygon
from vectorshape.reflection_point import ReflectionPoint
from vectorshape.shape import Shape
from vectorshape.vertice import Vertice


class SensorRect(Polygon):

    def __init__(self):
        pos_arr = (0, 0, k.VIEW_HEIGHT * k.PIXEL_SIZE)
        name = "DefaultScreen"
        super().__init__(pos_arr, name)
        self.add_vertice(Vertice(pos_arr, "TL"))
        self.add_vertice(Vertice((k.VIEW_WIDTH * k.PIXEL_SIZE, 0, k.VIEW_HEIGHT * k.PIXEL_SIZE), "TR"))
        self.add_vertice(Vertice((0, 0, 0), "BL"))
        self.add_vertice(Vertice((k.VIEW_WIDTH * k.PIXEL_SIZE, 0, 0), "BR"))

    @override
    def __repr__(self):
        return f'<ScreenRect "{self.name}": at [{self.pos[0]},{self.pos[1]},{self.pos[2]}] facing {str(self.normal) if self.normal is not None else "[]"} with [{",".join(v.get_name() for v in self.vertices_list)}]>'

    @override
    def calibrate_center(self):
        raise NotImplementedError(f"{self.__class__.__name__} does not implement calibrate_center")

    @override
    def ensure_normal_out(self, solid: Shape):
        raise NotImplementedError(f"{self.__class__.__name__} does not implement ensure_normal_out")

    @override
    def generate_plane(self) -> tuple[float, float, float, float]:
        if len(self.vertices_list) < 3:
            raise TypeError("polygon does not have enough vertices to generate a plane.")

        p = self.pos
        px = p[0]
        py = p[1]
        pz = p[2]

        v1 = self.vertices_list[1].get_pos() - p
        v2 = self.vertices_list[2].get_pos() - p

        normal = normpify_3vector(np.cross(v1, v2))
        if np.linalg.norm(normal) < k.EPSILON:
            raise ValueError("Degenerate polygon: cannot compute normal")
        self.normal = normal
        return self.plane_equation(px, py, pz)

    @override
    def generate_orthogonal_basis(self):
        if not self.verify_plane():
            raise ValueError("polygon has not been calibrated or does not have enough vertices to generate an orthogonal basis.")
        u = normpify_3vector(self.vertices_list[1].get_pos() - self.pos) * k.PIXEL_SIZE
        v = normpify_3vector(np.cross(self.normal, u)) * k.PIXEL_SIZE
        return u,v

    def open_shutter(self, reflections: list[ReflectionPoint]):
        to_render = []
        for reflection in reflections:
            if candidate := self.planar_ray_intersection(-self.normal, reflection.get_pos()) is not None:
                pass
        pass

