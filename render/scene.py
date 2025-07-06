import numpy as np

from Tests.test_helpers import create_test_cube
from tools import x_axis_rotation_matrix,y_axis_rotation_matrix, z_axis_rotation_matrix
from render.viewport import Viewport
from vectorshape.polygonal_solid import PolygonalSolid
from vectorshape.vertice import Vertice


class Scene():
    def __init__(self):
        self.viewport = Viewport()
        self.light_box = Vertice((0,-1,1), "LightBox")
        self.solids_actors: list[PolygonalSolid] =  []

    def setup(self):

        cube = create_test_cube()

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