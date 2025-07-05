from typing_extensions import override
import numpy as np

import default_constants as k
from tools import numpify_3vector, normpify_3vector, generate_ray_tracers, inverse_square_multiplier, plot_reflection_points
from vectorshape.polygon import Polygon
from vectorshape.reflection_point import ReflectionPoint
from vectorshape.shape import Shape
from vectorshape.vertice import Vertice


class PolygonalSolid(Shape):
    def __init__(self, pos_arr: tuple[float, float, float], this_way_up_arr: tuple[float, float, float], name: str):
        super().__init__(pos_arr, name)
        self.this_way_up = normpify_3vector(this_way_up_arr)
        self.faces: list[Polygon] = []

    @override
    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.name}": at [{self.pos[0]},{self.pos[1]},{self.pos[2]}] facing {str(self.this_way_up) if self.this_way_up is not None else "[]"} with [{",".join(f.get_name() for f in self.faces)}]>'

    @override
    def calibrate_center(self):
        vertices: list[Vertice] = []
        for face in self.faces:
            face.calibrate_center()
            face.ensure_normal_in(self)
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
    def rotate(self, matrices: list[np.ndarray], pivot_vec: tuple[float, float, float]=None):
        if pivot_vec is None:
            pivot_vec = self.pos
        pivot_vec = numpify_3vector(pivot_vec)
        for face in self.faces:
            face.rotate(matrices, pivot_vec)

    def add_face(self, face: Polygon):
        self.faces.append(face)


    def remove_face(self, face: Polygon):
        self.faces.remove(face)



    def make_reflection_points(self, light_box: Vertice) -> list[ReflectionPoint]:
        reflection_point_list = []
        rays = generate_ray_tracers()
        self.calibrate_center()
        for ray in rays:
            for face in self.faces:
                candidate = face.polygon_intersection_point(ray, self.pos)
                if candidate is None:
                    continue

                to_light_box = light_box.get_pos() - candidate
                face_unit = -normpify_3vector(face.get_normal())
                light_unit = normpify_3vector(to_light_box)
                distance_mult = inverse_square_multiplier(to_light_box)
                brightness = np.clip(np.dot(face_unit, light_unit) * distance_mult, 0, 1)
                reflection_point_list.append(ReflectionPoint(candidate, brightness, f"{face.get_name()}[{str(candidate)}] reflection"))
                break
        return reflection_point_list



