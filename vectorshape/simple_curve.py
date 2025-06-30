from vectorshape.line import Line
from vectorshape.vertice import Vertice


class SimpleCurve(Line):
    def __init__(self, vertices: tuple[Vertice, Vertice]):
        super().__init__(vertices)
