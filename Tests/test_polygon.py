import unittest
import numpy as np

from tools import numpify_3vector
from vectorshape.polygon import Polygon
from vectorshape.vertice import Vertice

class TestPolygon(unittest.TestCase):

    def setUp(self):
        self.polygon = Polygon((0, 0, 0), "poly")
        self.v1 = Vertice((1, 0, 0), "v1")
        self.v2 = Vertice((0, 1, 0), "v2")
        self.v3 = Vertice((0, 0, 0), "v3")

    def test_get_pos(self):
        np.testing.assert_array_equal(self.polygon.get_pos(), np.array([0.0, 0.0, 0.0]))

    def test_get_set_name(self):
        self.assertEqual(self.polygon.get_name(), "poly")
        self.polygon.set_name("new_name")
        self.assertEqual(self.polygon.get_name(), "new_name")

    def test_set_pos_moves_polygon_and_vertices(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        original_positions = [v.get_pos().copy() for v in self.polygon.get_vertices()]
        original_center = self.polygon.get_pos().copy()
        displacement = numpify_3vector((1, 1, 1)) - original_center
        self.polygon.set_pos((1, 1, 1))
        for old_pos, vert in zip(original_positions, self.polygon.get_vertices()):
            np.testing.assert_array_equal(vert.get_pos(), old_pos + displacement)

    def test_shift_position(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        original_center = self.polygon.get_pos().copy()
        self.polygon.shift_position((1, 2, 3))
        np.testing.assert_array_equal(self.polygon.get_pos(), numpify_3vector((1, 2, 3)) + original_center)
        for vert in self.polygon.get_vertices():
            self.assertTrue(np.all(vert.get_pos() >= np.array([1, 0, 0])))

    def test_generate_orthogonal_basis(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        u, v = self.polygon.generate_orthogonal_basis()
        dot_product = np.dot(u, v)
        self.assertAlmostEqual(dot_product, 0.0, delta=1e-6)
        self.assertAlmostEqual(np.linalg.norm(u), 1.0, delta=1e-6)
        self.assertAlmostEqual(np.linalg.norm(v), 1.0, delta=1e-6)

    def test_repr(self):
        self.polygon.add_vertice(self.v1)
        repr_str = repr(self.polygon)
        self.assertIn("poly", repr_str)
        self.assertIn("v1", repr_str)

    def test_generate_plane_degenerate_raises(self):
        with self.assertRaises(ValueError):
            v_same1 = Vertice((0, 0, 0), "v_same1")
            v_same2 = Vertice((0, 0, 0), "v_same2")
            v_same3 = Vertice((0, 0, 0), "v_same3")
            self.polygon.add_vertice(v_same1)
            self.polygon.add_vertice(v_same2)
            self.polygon.add_vertice(v_same3)

    def test_generate_plane_valid(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        a, b, c, d = self.polygon.generate_plane()
        self.assertTrue(np.linalg.norm([a, b, c]) > 0)

    def test_coplanar_position_by_basis(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        copos = self.v1.get_pos()
        result = self.polygon.coplanar_position_by_basis(copos)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)

    def test_point_in_polygon_3d_and_2d(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        inside = self.polygon.point_in_polygon_3d((0.25, 0.25, 0))
        outside = self.polygon.point_in_polygon_3d((2, 2, 0))
        self.assertTrue(inside)
        self.assertFalse(outside)

    def test_planar_ray_intersection(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        point = self.polygon.planar_ray_intersection((0, 0, -1), (0.25, 0.25, 1))
        self.assertIsNotNone(point)
        np.testing.assert_almost_equal(point[2], 0.0, decimal=6)

    def test_polygon_intersection_point(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        hit = self.polygon.polygon_intersection_point((0, 0, -1), (0.25, 0.25, 1))
        miss = self.polygon.polygon_intersection_point((0, 0, -1), (5, 5, 1))
        self.assertIsNotNone(hit)
        self.assertIsNone(miss)

    def test_remove_vertice(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        self.polygon.remove_vertice(self.v1)
        self.assertEqual(len(self.polygon.get_vertices()), 2)
        self.assertIsNone(self.polygon.normal)

    def test_project(self):
        self.polygon.add_vertice(self.v1)
        self.polygon.add_vertice(self.v2)
        self.polygon.add_vertice(self.v3)
        q = (0.25, 0.25, 0)
        projected = self.polygon.project(q)
        self.assertEqual(projected.shape, (2,))

if __name__ == '__main__':
    unittest.main()