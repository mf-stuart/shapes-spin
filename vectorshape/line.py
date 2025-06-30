import numpy as np

from vectorshape.edge import Edge
from vectorshape.vertice import Vertice

class Line(Edge):
    def __init__(self, vertices: tuple[Vertice, Vertice], visible: bool = True):
        super().__init__(vertices)
        self.visible: bool = visible

    def render(self):
        pass

