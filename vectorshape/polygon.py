import numpy as np
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
        return f'<Polygon "{self.name}": at [{self.pos[0]},{self.pos[1]},{self.pos[2]}] facing {str(self.normal) if self.normal is not None else "[]"} with [{",".join(v.get_name() for v in self.vertices_list)}]>'

    @override
    def set_pos(self, pos_arr: tuple[float, float, float]):
        pos_arr = numpify_3vector(pos_arr)
        displacement_vector = pos_arr - self.pos
        self.shift_position(displacement_vector)

    @override
    def calibrate_center(self):
        self.pos = np.mean([vertice.get_pos() for vertice in self.vertices_list], axis=0)

    @override
    def shift_position(self, movement_vec: tuple[float, float, float]):
        movement_vec = numpify_3vector(movement_vec)
        self.pos += movement_vec
        for vertice in self.vertices_list:
            vertice.set_pos(vertice.get_pos() + movement_vec)

    @override
    def rotate(self, matrix: np.array, pivot_vec: tuple[float, float, float]):
        pass

    def add_vertice(self, vertice: Vertice):
        if vertice not in self.vertices_list and self.new_vertex_fits(vertice):
            self.vertices_list.append(vertice)

    def new_vertex_fits(self, vertice: Vertice):
        if self.normal is None:
            return True
        return np.dot(vertice.get_pos() - self.pos, self.normal) < k.EPSILON

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

        a, b, c = self.normal
        d = -(a*px + b*py + c*pz)
        self.plane_eq = np.array([a, b, c, d])

        return a, b, c, d

    def verify_plane(self) -> bool:
        return self.normal is not None and len(self.vertices_list) >= 3

    def ensure_normal_out(self, solid: Shape):
        if len(self.vertices_list) < 3:
            raise TypeError("polygon does not have enough vertices to generate a plane.")
        to_face = self.vertices_list[0].get_pos() - solid.get_pos()
        if np.dot(to_face, self.normal) < 0:
            self.normal = -self.normal

    def get_normal(self) -> np.ndarray:
        return self.normal

    def generate_orthogonal_basis(self):
        if self.verify_plane():
            U = normpify_3vector(self.vertices_list[0].get_pos() - self.pos)
            V = normpify_3vector(np.cross(self.normal, U))
            return (U,V)
        return None


    def polygon_collision_point(self, ray_vector: tuple[float, float, float], origin: tuple[float, float, float])-> np.ndarray:
        candidate_point = self.planar_ray_intersection(ray_vector, origin)
        if candidate_point is not None and self.point_in_polygon_3D(candidate_point) is not None:
            return candidate_point
        return None

    def planar_ray_intersection(self, ray_vector: tuple[float, float, float], origin: tuple[float, float, float]) -> np.ndarray:
        origin = numpify_3vector(origin)
        ray_vector = normpify_3vector(ray_vector)
        p0 = self.pos

        if np.dot(self.normal, ray_vector) < 0:
            return None

        t = np.dot(p0 - origin, self.normal) / np.dot(ray_vector, self.normal)
        candidate_point = origin + t * ray_vector
        return numpify_3vector(candidate_point)

    def point_in_polygon_3D(self, Q: tuple[float, float, float]) -> bool:
        if not self.verify_plane():
            return False
        Q = numpify_3vector(Q)
        a, b, c, d = self.plane_eq
        if abs(Q[0]*a + Q[1]*b + Q[2]*c + d) > k.EPSILON:
            return False
        Q_2d = self.project(Q)
        return self.point_in_polygon_2D(Q_2d)

    def point_in_polygon_2D(self, q: tuple[float, float]) -> bool:
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


    def project(self, Q: tuple[float, float, float]) -> np.ndarray:
        if self.verify_plane():
            Q = numpify_3vector(Q)
            U, V = self.generate_orthogonal_basis()
            return  numpify_2vector([np.dot(Q - self.vertices_list[0].get_pos(), U), np.dot(Q - self.vertices_list[0].get_pos(), V)])
        return None