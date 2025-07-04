import unittest
import numpy as np
import numpy.testing as npt
from typing_extensions import override

import default_constants as k
from tools import z_axis_rotation_matrix
from test_shape import TestShape
from vectorshape.polygon import Polygon
from vectorshape.vertice import Vertice


class TestPolygon(TestShape):

    def setUp(self):
        self.pos_instantiate = (3.0, 3.0, 1.0)
        self.name = "poly"
        self.shape = Polygon(self.pos_instantiate, self.name)

        self.v1 = Vertice((0.0, 0.0, 0.0), "v1")
        self.v2 = Vertice((1.0, 0.0, 0.0), "v2")
        self.v3 = Vertice((0.0, 1.0, 0.0), "v3")

        self.shape.add_vertice(self.v1)
        self.shape.add_vertice(self.v2)
        self.shape.add_vertice(self.v3)

        # testPrint(self.shape)

    @override
    def test_set_pos(self):
        old_pos = self.shape.get_pos().copy()
        old_v1_pos = self.v1.get_pos().copy()
        old_v2_pos = self.v2.get_pos().copy()
        old_v3_pos = self.v3.get_pos().copy()

        new_pos = (5.0, 5.0, 1.0)
        displacement = np.array(new_pos) - old_pos

        self.shape.set_pos(new_pos)

        npt.assert_array_almost_equal(self.shape.get_pos(), new_pos)
        npt.assert_array_almost_equal(self.v1.get_pos(), old_v1_pos + displacement)
        npt.assert_array_almost_equal(self.v2.get_pos(), old_v2_pos + displacement)
        npt.assert_array_almost_equal(self.v3.get_pos(), old_v3_pos + displacement)

    def test_calibrate_center(self):
        self.v1.set_pos((1.0, 0.0, 0.0))
        self.v2.set_pos((0.0, 1.0, 0.0))
        self.v3.set_pos((0.0, 0.0, 1.0))
        self.shape.calibrate_center()
        expected_center = np.mean([self.v1.get_pos(), self.v2.get_pos(), self.v3.get_pos()], axis=0)
        npt.assert_array_almost_equal(self.shape.get_pos(), expected_center)

    def test_shift_position(self):
        initial_pos = self.shape.get_pos().copy()
        movement = (1.0, 2.0, 3.0)
        self.shape.shift_position(movement)
        npt.assert_array_almost_equal(self.shape.get_pos(), initial_pos + np.array(movement))

    def test_rotate(self):
        angle = np.pi / 2
        rz = z_axis_rotation_matrix(angle)

        old_positions = [v.get_pos() - self.shape.get_pos() for v in self.shape.get_vertices()]
        expected_positions = [rz @ pos + self.shape.get_pos() for pos in old_positions]

        from unittest.mock import patch
        with patch.object(self.shape, 'generate_plane', wraps=self.shape.generate_plane) as mock_gen_plane:
            self.shape.rotate([rz])
            mock_gen_plane.assert_called_once()

        for vert, expected in zip(self.shape.get_vertices(), expected_positions):
            npt.assert_array_almost_equal(vert.get_pos(), expected)

    def test_add_and_remove_vertices(self):
        self.assertEqual(len(self.shape.get_vertices()), 3)
        self.assertIn(self.v2, self.shape.get_vertices())

        self.shape.remove_vertice(self.v2)
        self.assertEqual(len(self.shape.get_vertices()), 2)
        self.assertNotIn(self.v2, self.shape.get_vertices())

    def test_generate_plane_and_normal(self):
        plane = self.shape.generate_plane()

        expected_normal = np.array([0.0, 0.0, 1.0])
        npt.assert_array_almost_equal(self.shape.get_normal(), expected_normal)
        self.assertEqual(len(plane), 4)

    def test_point_in_polygon_3d(self):
        self.shape.generate_plane()

        inside_point = (0.25, 0.25, 0.0)
        outside_point = (1.0, 1.0, 0.0)
        on_edge_point = (0.5, 0.0, 0.0)
        on_vertex_point = (0.0, 0.0, 0.0)
        above_polygon = (0.25, 0.25, 1.0)
        below_polygon = (0.25, 0.25, -1.0)

        self.assertTrue(self.shape.point_in_polygon_3d(inside_point))
        self.assertFalse(self.shape.point_in_polygon_3d(outside_point))
        self.assertTrue(self.shape.point_in_polygon_3d(on_edge_point))
        self.assertTrue(self.shape.point_in_polygon_3d(on_vertex_point))

        self.assertFalse(self.shape.point_in_polygon_3d(above_polygon))
        self.assertFalse(self.shape.point_in_polygon_3d(below_polygon))

    def test_generate_orthogonal_basis(self):
        self.shape.generate_plane()
        u, v = self.shape.generate_orthogonal_basis()
        dot_product = np.dot(u, v)
        self.assertAlmostEqual(dot_product, 0.0, delta=k.EPSILON)
        self.assertAlmostEqual(np.linalg.norm(u), 1, delta=k.EPSILON)
        self.assertAlmostEqual(np.linalg.norm(v), 1, delta=k.EPSILON)

    def test_verify_coplanarity(self):
        self.shape.generate_plane()
        coplanar_point = self.v1.get_pos()
        off_plane_point = coplanar_point + np.array([0.0, 0.0, 1.0])
        self.assertTrue(self.shape.verify_coplanarity(coplanar_point))
        self.assertFalse(self.shape.verify_coplanarity(off_plane_point))

    def test_coplanar_position_by_basis(self):
        self.shape.generate_plane()
        pos = self.v1.get_pos()
        alpha_beta = self.shape.coplanar_position_by_basis(pos)
        self.assertIsNotNone(alpha_beta)
        alpha, beta = alpha_beta
        self.assertIsInstance(alpha, float)
        self.assertIsInstance(beta, float)

    def test_polygon_intersection_point(self):
        self.shape.generate_plane()
        ray_origin = self.shape.get_pos() + np.array([0.0, 0.0, 1.0])
        ray_vector = np.array([0.0, 0.0, -1.0])
        intersection = self.shape.polygon_intersection_point(ray_vector, ray_origin)
        self.assertIsNotNone(intersection)
        self.assertTrue(self.shape.point_in_polygon_3d(intersection))

    def test_ensure_normal_out(self):
        class MockSolid:
            def __init__(self, pos):
                self.pos = np.array(pos)

            def get_pos(self):
                return self.pos

        self.shape.generate_plane()
        solid = MockSolid((0.0, 0.0, 0.0))
        self.shape.ensure_normal_out(solid)
        to_face = self.v1.get_pos() - solid.get_pos()
        self.assertGreaterEqual(np.dot(to_face, self.shape.get_normal()), 0.0)


if __name__ == '__main__':
    unittest.main()