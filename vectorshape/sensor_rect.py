import numpy as np
import default_constants as k

from typing import override

from render.pixel_data import PixelData
from tools import normpify_3vector, numpify_3vector, plot_pixel_data, numpify_2vector
from vectorshape.polygon import Polygon
from vectorshape.reflection_point import ReflectionPoint
from vectorshape.shape import Shape
from vectorshape.vertice import Vertice


class SensorRect(Polygon):

    def __init__(self):
        name = "DefaultScreen"
        pos_arr = (0,-12,0)
        super().__init__(pos_arr, name)
        self.camera_pos = None
        width = k.VIEW_WIDTH * k.PIXEL_SIZE
        height = k.VIEW_HEIGHT * k.PIXEL_SIZE

        # Vertices relative to center
        hw = 0.5 * width
        hh = 0.5 * height

        self.add_vertice(Vertice((pos_arr[0] - hw, pos_arr[1], pos_arr[2] + hh), "TL"))  # Top Left
        self.add_vertice(Vertice((pos_arr[0] + hw, pos_arr[1], pos_arr[2] + hh), "TR"))  # Top Right
        self.add_vertice(Vertice((pos_arr[0] + hw, pos_arr[1], pos_arr[2] - hh), "BR"))  # Bottom Right
        self.add_vertice(Vertice((pos_arr[0] - hw, pos_arr[1], pos_arr[2] - hh), "BL"))  # Bottom Left

        self.generate_plane()


    @override
    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.name}": at [{self.pos[0]},{self.pos[1]},{self.pos[2]}] facing {str(self.normal) if self.normal is not None else "[]"} with [{",".join(v.get_name() for v in self.vertices_list)}]>'

    @override
    def set_pos(self, pos_arr: tuple[float, float, float]):
        super().set_pos(pos_arr)
        self._update_camera_position()

    @override
    def shift_position(self, displacement_vector: tuple[float, float, float]):
        super().shift_position(displacement_vector)
        self._update_camera_position()

    @override
    def rotate(self, matrices: list[np.ndarray], pivot_vec: tuple[float, float, float] = None):
        super().rotate(matrices, pivot_vec)
        self._update_camera_position()

    @override
    def calibrate_center(self):
        super().calibrate_center()
        if not self.verify_plane():
            raise RuntimeError("Cannot calibrate a camera position without a plane.")
        self.camera_pos = self.pos - k.CAMERA_DEPTH * self.normal

    @override
    def ensure_normal_in(self, solid: Shape):
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
        self.calibrate_center()
        return self.plane_equation(px, py, pz)

    @override
    def generate_orthogonal_basis(self):
        if not self.verify_plane():
            raise ValueError(
                "polygon has not been calibrated or does not have enough vertices to generate an orthogonal basis.")
        u = normpify_3vector(self.vertices_list[1].get_pos() - self.vertices_list[0].get_pos())
        v = normpify_3vector(np.cross(u, self.normal))
        return u, v

    @override
    def project(self, q: tuple[float, float, float]) -> np.ndarray:
        if not self.verify_plane():
            raise ValueError("plane could not be established for projection")
        q = numpify_3vector(q)
        u, v = self.generate_orthogonal_basis()
        origin = self.vertices_list[0].get_pos()
        diff = q - origin

        u_proj = np.dot(diff, u) / np.dot(u, u)
        v_proj = np.dot(diff, v) / np.dot(v, v)

        return numpify_2vector([u_proj, v_proj])

    def _update_camera_position(self):
        self.calibrate_center()

    def find_pixel_coordinate_from_projection(self, coplanar_pos: tuple[float, float, float]) -> tuple[float, float]:
        planar_vec  = self.project(coplanar_pos)
        alpha = float(planar_vec[0] / k.PIXEL_SIZE)
        beta = float(planar_vec[1] / k.PIXEL_SIZE)
        return alpha, -beta

    def open_shutter(self, reflections: list[ReflectionPoint]):
        to_render = []
        for reflection in reflections:
            perspective_vector = numpify_3vector(self.camera_pos - reflection.get_pos())

            # perspective_vector = numpify_3vector(-self.normal)

            candidate = self.polygon_intersection_point(perspective_vector, reflection.get_pos())
            if candidate is None:
                continue

            rough_indices = self.find_pixel_coordinate_from_projection(candidate)
            indices = tuple(map(int, map(np.round, rough_indices)))
            length = np.linalg.norm(self.camera_pos - reflection.get_pos())
            brightness = reflection.get_brightness()
            to_render.append(PixelData(indices, brightness, length))
        plot_pixel_data(to_render)
        return to_render