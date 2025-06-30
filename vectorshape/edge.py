from vectorshape.vertice import Vertice


class Edge:
    def __init__(self, vertices: tuple[Vertice], length: float):
        self.vertices = vertices
        self.length = length