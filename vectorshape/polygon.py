import numpy as np

from functools import reduce
from typing_extensions import override

import default_constants as k
from tools import normpify_3vector, numpify_3vector, numpify_2vector
from vectorshape.shape import Shape
from vectorshape.vertice import Vertice

class Polygon(Shape):
    def __init__(self, pos_arr: tuple[float, float, float], name: str):
        super().__init__(pos_arr, name)
        self.normal: np.array = None
        self.plane_eq: np.array = None
        self.vertices_list: list[Vertice] = []

    @override
    def __repr__(self):
        return f'<{self.__class__} "{self.name}": at [{self.pos[0]},{self.pos[1]},{self.pos[2]}] facing {str(self.normal) if self.normal is not None else "[]"} with [{",".join(v.get_name() for v in self.vertices_list)}]>'

    @override
    def set_pos(self, pos_arr: tuple[float, float, float]):
        pos_arr = numpify_3vector(pos_arr)
        displacement_vector = pos_arr - self.pos
        self.shift_position(displacement_vector)

    @override
    def shift_position(self, movement_vec: tuple[float, float, float]):
        movement_vec = numpify_3vector(movement_vec)
        self.pos += movement_vec
        for vertice in self.vertices_list:
            vertice.set_pos(vertice.get_pos() + movement_vec)

    @override
    def calibrate_center(self):
        self.pos = np.mean([vertice.get_pos() for vertice in self.vertices_list], axis=0)

    @override
    def rotate(self, matrices: list[np.ndarray], pivot_vec: tuple[float, float, float]=None):
        if pivot_vec is None:
            pivot_vec = self.pos

        pivot_vec = numpify_3vector(pivot_vec)
        translated_vertices_positions = [v.get_pos() - self.pos for v in self.vertices_list]
        r_matrix = reduce(np.matmul, matrices)

        rotated_vertices_positions = [r_matrix @ tv for tv in translated_vertices_positions]
        resolved_vertices_position = [v + pivot_vec for v in rotated_vertices_positions]

        for vert, new_pos in zip(self.vertices_list, resolved_vertices_position):
            vert.set_pos(new_pos)
        self.generate_plane()

    def add_vertice(self, vertice: Vertice):
        if vertice not in self.vertices_list and self.new_vertex_fits(vertice):
            self.vertices_list.append(vertice)

    def new_vertex_fits(self, vertice: Vertice):
        if self.normal is None:
            return True
        return abs(np.dot(vertice.get_pos() - self.pos, self.normal)) < k.EPSILON

    def remove_vertice(self, vertice: Vertice):
        self.vertices_list.remove(vertice)
        if len(self.vertices_list) < 3:
            self.normal = None
            self.plane_eq = None

    def get_vertices(self) -> list[Vertice]:
        return self.vertices_list

    def generate_plane(self) -> tuple[float, float, float, float]:
        if len(self.vertices_list) < 3:
            raise TypeError("polygon does not have enough vertices to generate a plane.")

        self.calibrate_center()

        p = self.pos
        px = p[0]
        py = p[1]
        pz = p[2]

        v1 = self.vertices_list[0].get_pos() - p
        v2 = self.vertices_list[1].get_pos() - p

        normal = normpify_3vector(np.cross(v1, v2))
        if np.linalg.norm(normal) < k.EPSILON:
            raise ValueError("Degenerate polygon: cannot compute normal")
        self.normal = normal
        return self.plane_equation(px, py, pz)

    def plane_equation(self, px, py, pz):
        a, b, c = self.normal
        d = -(a * px + b * py + c * pz)
        self.plane_eq = np.array([a, b, c, d])
        return a, b, c, d

    def verify_plane(self) -> bool:
        return self.normal is not None and len(self.vertices_list) >= 3

    def verify_coplanarity(self, pos: tuple[float, float, float]) -> bool:
        if self.verify_plane():
            pos = numpify_3vector(pos)
            return abs(np.dot(pos - self.pos, self.normal)) < k.EPSILON
        return False

    def ensure_normal_out(self, solid: Shape):
        if not self.verify_plane():
            raise ValueError("polygon has not been calibrated or does not have enough vertices to generate a plane.")
        to_face = self.vertices_list[0].get_pos() - solid.get_pos()
        if np.dot(to_face, self.normal) < 0:
            self.normal = -self.normal

    def get_normal(self) -> np.ndarray:
        return self.normal

    def generate_orthogonal_basis(self):
        if not self.verify_plane():
            raise ValueError("polygon has not been calibrated or does not have enough vertices to generate an orthogonal basis.")
        u = normpify_3vector(self.vertices_list[0].get_pos() - self.pos)
        v = normpify_3vector(np.cross(self.normal, u))
        return u,v

    def coplanar_position_by_basis(self, coplanar_pos: tuple[float, float, float]) -> tuple[float, float]:
        coplanar_pos = numpify_3vector(coplanar_pos)
        coplanar_vec = coplanar_pos - self.pos
        if self.verify_coplanarity(coplanar_pos):
            u, v = self.generate_orthogonal_basis()
            alpha = np.dot(coplanar_vec, u) / np.dot(u, u)
            beta = np.dot(coplanar_vec, v) / np.dot(v, v)
            return alpha, beta
        return None

    def polygon_intersection_point(self, ray_vector: tuple[float, float, float], origin: tuple[float, float, float]) -> np.ndarray:
        candidate_point = self.planar_ray_intersection(ray_vector, origin)
        if candidate_point is not None and self.point_in_polygon_3d(candidate_point) is not None:
            return candidate_point
        return None

    def planar_ray_intersection(self, ray_vector: tuple[float, float, float], origin: tuple[float, float, float]) -> np.ndarray:
        if not self.verify_plane():
            raise ValueError("plane could not be established for ray intersection")

        origin = numpify_3vector(origin)
        ray_vector = normpify_3vector(ray_vector)
        denom = np.dot(self.normal, ray_vector)

        if denom > -k.EPSILON:
            return None

        t = np.dot(self.pos - origin, self.normal) / denom
        if t < 0:
            return None

        candidate_point = origin + t * ray_vector
        return numpify_3vector(candidate_point)

    def point_in_polygon_3d(self, q: tuple[float, float, float]) -> bool:
        if not self.verify_plane():
            return False
        q = numpify_3vector(q)
        a, b, c, d = self.plane_eq
        if abs(q[0] * a + q[1] * b + q[2] * c + d) > k.EPSILON:
            return False
        q_2d = self.project(q)
        return self.point_in_polygon_2d(q_2d)

    def point_in_polygon_2d(self, q: tuple[float, float]) -> bool:
        if not self.verify_plane():
            return False
        q = numpify_2vector(q)
        polygon_2d = [self.project(vertice.get_pos()) for vertice in self.vertices_list]

        vert_count = len(polygon_2d)
        prev_cross = None
        for i in range(vert_count):
            vertice_a = polygon_2d[i]
            vertice_b = polygon_2d[(i+1) % vert_count]
            edge = vertice_b - vertice_a
            to_point = q - vertice_a

            cross_z = edge[0] * to_point[1] - edge[1] * to_point[0]
            if abs(cross_z) < k.EPSILON:
                continue
            if prev_cross is None:
                prev_cross = cross_z
            elif cross_z * prev_cross < -k.EPSILON:
                return False
        return True

    def project(self, q: tuple[float, float, float]) -> np.ndarray:
        if self.verify_plane():
            q = numpify_3vector(q)
            u, v = self.generate_orthogonal_basis()
            return  numpify_2vector([np.dot(q - self.vertices_list[0].get_pos(), u), np.dot(q - self.vertices_list[0].get_pos(), v)])
        return None