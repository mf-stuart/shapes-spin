from vectorshape.polygon import Polygon
from vectorshape.polygonal_solid import PolygonalSolid
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

def create_test_cube():
    cube_vertices = [
        Vertice((3, 11, 3), "v0"),  # top front right
        Vertice((-3, 11, 3), "v1"),  # top front left
        Vertice((-3, 5, 3), "v2"),  # bottom front left
        Vertice((3, 5, 3), "v3"),  # bottom front right

        Vertice((3, 11, -3), "v4"),  # top back right
        Vertice((-3, 11, -3), "v5"),  # top back left
        Vertice((-3, 5, -3), "v6"),  # bottom back left
        Vertice((3, 5, -3), "v7"),  # bottom back right
    ]

    v = cube_vertices  # shorthand

    faces = []

    # Top face
    top = Polygon(v[0].get_pos(), "Top")
    top.add_vertice(v[0])
    top.add_vertice(v[1])
    top.add_vertice(v[2])
    top.add_vertice(v[3])
    top.generate_plane()
    faces.append(top)

    # Bottom face
    bottom = Polygon(v[4].get_pos(), "Bottom")
    bottom.add_vertice(v[4])
    bottom.add_vertice(v[5])
    bottom.add_vertice(v[6])
    bottom.add_vertice(v[7])
    bottom.generate_plane()
    faces.append(bottom)

    # Front face
    front = Polygon(v[0].get_pos(), "Front")
    front.add_vertice(v[0])
    front.add_vertice(v[1])
    front.add_vertice(v[5])
    front.add_vertice(v[4])
    front.generate_plane()
    faces.append(front)

    # Back face
    back = Polygon(v[3].get_pos(), "Back")
    back.add_vertice(v[3])
    back.add_vertice(v[2])
    back.add_vertice(v[6])
    back.add_vertice(v[7])
    back.generate_plane()
    faces.append(back)

    # Right face
    right = Polygon(v[0].get_pos(), "Right")
    right.add_vertice(v[0])
    right.add_vertice(v[3])
    right.add_vertice(v[7])
    right.add_vertice(v[4])
    right.generate_plane()
    faces.append(right)

    # Left face
    left = Polygon(v[1].get_pos(), "Left")
    left.add_vertice(v[1])
    left.add_vertice(v[2])
    left.add_vertice(v[6])
    left.add_vertice(v[5])
    left.generate_plane()
    faces.append(left)

    cube = PolygonalSolid((5, 5, 5), (0, 0, 1), "UnitCube")
    for face in faces:
        cube.add_face(face)
    cube.calibrate_center()
    return cube