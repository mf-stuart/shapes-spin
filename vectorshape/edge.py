import numpy as np
from vectorshape.vertice import Vertice


class Edge:
    def __init__(self, vertices: tuple[Vertice, Vertice]):

        assert len(vertices) == 2, "exactly 2 vertices were not given"
        assert not np.all(vertices[0].get_pos() == vertices[1].get_pos()), \
            "first vertex was the same as second vertex"

        self.vertices: tuple[Vertice, Vertice] = vertices

        self.dir_vector: np.array = None
        self.length: float = None
        self.angles: np.array = None

        self.build()

    def build(self):
        self.dir_vector = self.vertices[0].get_pos() - self.vertices[1].get_pos()
        self.length = np.linalg.norm(self.dir_vector)
        self.build_angles()

    def build_angles(self) -> None:
        zenith  = float(np.acos( self.dir_vector[2] / self.length ))
        azimuth = float(np.arctan2( self.dir_vector[1], self.dir_vector[0] ))
        self.angles = np.array([azimuth, zenith])

    def get_angle(self) -> np.ndarray[float]:
        return self.angles

    def set_vertices(self, vertices: tuple[Vertice, Vertice]):
        self.vertices = vertices
        self.build()

    def get_vertices(self) -> tuple[Vertice, Vertice]:
        return self.vertices
