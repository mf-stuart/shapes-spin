from vectorshape.polygon import Polygon
from vectorshape.vertice import Vertice

def create_basic_polygon():
    poly = Polygon((0, 0, 0), "basic")
    v1 = Vertice((0, 0, 0), "v1")
    v2 = Vertice((1, 0, 0), "v2")
    v3 = Vertice((0, 1, 0), "v3")
    poly.add_vertice(v1)
    poly.add_vertice(v2)
    poly.add_vertice(v3)
    return poly, v1, v2, v3