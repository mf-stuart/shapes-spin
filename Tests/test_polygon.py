import unittest
import numpy as np

from vectorshape.vertice import Vertice
from vectorshape.polygon import Polygon
from vectorshape.polygonal_solid import PolygonalSolid

class TestPolygonalSolid(unittest.TestCase):

    def setUp(self):
        self.vertices = [
            Vertice((1, 1, 1), "v0"),
            Vertice((-1, 1, 1), "v1"),
            Vertice((-1, -1, 1), "v2"),
            Vertice((1, -1, 1), "v3"),
            Vertice((1, 1, -1), "v4"),
            Vertice((-1, 1, -1), "v5"),
            Vertice((-1, -1, -1), "v6"),
            Vertice((1, -1, -1), "v7"),
        ]

        self.faces = [
            Polygon((0,0,1), "front"),
            Polygon((0,0,-1), "back"),
            Polygon((0,1,0), "top"),
            Polygon((0,-1,0), "bottom"),
            Polygon((1,0,0), "right"),
            Polygon((-1,0,0), "left"),
        ]

        self.faces[0].add_vertice(self.vertices[0])
        self.faces[0].add_vertice(self.vertices[1])
        self.faces[0].add_vertice(self.vertices[2])
        self.faces[0].add_vertice(self.vertices[3])

        self.faces[1].add_vertice(self.vertices[4])
        self.faces[1].add_vertice(self.vertices[5])
        self.faces[1].add_vertice(self.vertices[6])
        self.faces[1].add_vertice(self.vertices[7])

        self.faces[2].add_vertice(self.vertices[0])
        self.faces[2].add_vertice(self.vertices[1])
        self.faces[2].add_vertice(self.vertices[5])
        self.faces[2].add_vertice(self.vertices[4])

        self.faces[3].add_vertice(self.vertices[3])
        self.faces[3].add_vertice(self.vertices[2])
        self.faces[3].add_vertice(self.vertices[6])
        self.faces[3].add_vertice(self.vertices[7])

        self.faces[4].add_vertice(self.vertices[0])
        self.faces[4].add_vertice(self.vertices[3])
        self.faces[4].add_vertice(self.vertices[7])
        self.faces[4].add_vertice(self.vertices[4])

        self.faces[5].add_vertice(self.vertices[1])
        self.faces[5].add_vertice(self.vertices[2])
        self.faces[5].add_vertice(self.vertices[6])
        self.faces[5].add_vertice(self.vertices[5])

        self.solid = PolygonalSolid(self.faces)

    def test_vertex_count(self):
        self.assertEqual(len(self.solid.vertices), 8)

    def test_face_count(self):
        self.assertEqual(len(self.solid.faces), 6)

    def test_normals_point_inwards(self):
        center = self.solid.center()
        for face in self.solid.faces:
            normal = face.normal
            face_center = np.mean([v.get_pos() for v in face.get_vertices()], axis=0)
            vec = center - face_center
            self.assertGreater(np.dot(normal, vec), 0)

    def test_volume_positive(self):
        vol = self.solid.compute_volume()
        self.assertGreater(vol, 0)

    def test_contains_point_inside(self):
        point = np.array([0, 0, 0])
        self.assertTrue(self.solid.contains_point(point))

    def test_contains_point_outside(self):
        point = np.array([3, 3, 3])
        self.assertFalse(self.solid.contains_point(point))

    def test_translate_solid(self):
        original_center = self.solid.center()
        translation = np.array([1, 2, 3])
        self.solid.translate(translation)
        new_center = self.solid.center()
        np.testing.assert_array_almost_equal(new_center, original_center + translation)

    def test_rotate_solid(self):
        angle = np.radians(45)
        axis = np.array([0, 0, 1])
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        original_positions = [v.get_pos().copy() for v in self.solid.vertices]
        self.solid.rotate([rotation_matrix])
        rotated_positions = [v.get_pos() for v in self.solid.vertices]
        for orig, rotated in zip(original_positions, rotated_positions):
            expected = rotation_matrix @ orig
            np.testing.assert_array_almost_equal(rotated, expected)

if __name__ == "__main__":
    unittest.main()
