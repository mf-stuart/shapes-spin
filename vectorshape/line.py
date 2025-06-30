import numpy as np

from vectorshape.edge import Edge
from vectorshape.vertice import Vertice

class Line(Edge):
    def __init__(self, vertices: tuple[Vertice], length: float):
        super().__init__(vertices, length)

