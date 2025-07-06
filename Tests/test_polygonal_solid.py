import unittest
import numpy as np

from test_helpers import create_test_cube
from vectorshape.vertice import Vertice
from vectorshape.polygon import Polygon
from vectorshape.polygonal_solid import PolygonalSolid
from tools import numpify_3vector

class TestPolygonalSolid(unittest.TestCase):

    def setUp(self):
        self.solid = create_test_cube()

    def test_add_and_remove_face(self):
        face = Polygon((1, 0, 0), "TestFace")
        self.solid.add_face(face)
        self.assertIn(face, self.solid.faces)
        self.solid.remove_face(face)
        self.assertNotIn(face, self.solid.faces)

    def test_calibrate_center(self):
        self.solid.calibrate_center()
        vertices = []
        for face in self.solid.faces:
            for v in face.get_vertices():
                if v not in vertices:
                    vertices.append(v)
        expected_center = np.mean([v.get_pos() for v in vertices], axis=0)
        np.testing.assert_array_almost_equal(self.solid.get_pos(), expected_center)

    def test_shift_position(self):
        old_positions = [v.get_pos().copy() for v in self.solid.get_vertices()]
        movement = (1, 2, 3)
        self.solid.shift_position(movement)
        new_positions = [v.get_pos() for face in self.solid.faces for v in face.get_vertices()]
        for old, new in zip(old_positions, new_positions):
            np.testing.assert_array_almost_equal(new, old + numpify_3vector(movement))
        np.testing.assert_array_almost_equal(self.solid.get_pos(), numpify_3vector(movement) + np.array([0,8,0]))

    def test_rotate_default_pivot(self):
        # TODO: This
        pass

    def test_rotate_faces_plane_regenerated(self):
        # TODO: This
        pass

if __name__ == "__main__":
    unittest.main()
