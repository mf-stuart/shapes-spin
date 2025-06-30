import numpy as np

from vectorshape.line import Line
from vectorshape.vertice import Vertice

class BezierCurve(Line):
    def __init__(self, vertices: tuple[Vertice, Vertice], bezier_anchor: tuple[float, float, float]):
        super().__init__(vertices)
        self.bezier_anchor: np.array = np.array(bezier_anchor)

    def build(self):
        super().build()