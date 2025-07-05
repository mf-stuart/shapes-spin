import numpy as np

from tools import x_axis_rotation_matrix,y_axis_rotation_matrix, z_axis_rotation_matrix
from render.viewport import Viewport
from vectorshape.polygon import Polygon
from vectorshape.polygonal_solid import PolygonalSolid
from vectorshape.vertice import Vertice


class Scene():
    def __init__(self):
        self.viewport = Viewport()
        self.light_box = Vertice((30,-30,30), "LightBox")
        self.solids_actors: list[PolygonalSolid] =  []

    def setup(self):
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

        cube = PolygonalSolid((5,5,5), (0,0,1),"UnitCube")
        for face in faces:
            cube.add_face(face)
        cube.calibrate_center()

        matrices =[
            x_axis_rotation_matrix(np.radians(35.264)),
            z_axis_rotation_matrix(np.radians(45))
        ]
        cube.rotate(matrices)

        self.solids_actors.append(cube)

    def render_frame(self):
        reflection_points = []
        for actor in self.solids_actors:
            reflection_points.extend(actor.make_reflection_points(self.light_box))
        pixel_points =  self.viewport.get_sensor_plane().open_shutter(reflection_points)
        self.viewport.render_ascii(pixel_points)

if __name__ == "__main__":
    scene = Scene()
    scene.setup()
    scene.render_frame()