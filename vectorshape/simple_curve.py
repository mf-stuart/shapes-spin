from vectorshape.edge import Edge
from vectorshape.vertice import Vertice



class SimpleCurve(Edge):
    def __init__(self, vertices: tuple[Vertice], length: float):
        super().__init__(vertices, length)