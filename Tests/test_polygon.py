import unittest
import numpy as np
import numpy.testing as npt
from typing_extensions import override

from test_shape import TestShape
from vectorshape.shape import Shape
from vectorshape.polygon import Polygon
from vectorshape.vertice import Vertice
from tools import numpify_3vector, testPrint


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
        pass

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

        self.assertTrue(self.shape.point_in_polygon_3D(inside_point))
        self.assertFalse(self.shape.point_in_polygon_3D(outside_point))
        self.assertTrue(self.shape.point_in_polygon_3D(on_edge_point))
        self.assertTrue(self.shape.point_in_polygon_3D(on_vertex_point))

        self.assertFalse(self.shape.point_in_polygon_3D(above_polygon))
        self.assertFalse(self.shape.point_in_polygon_3D(below_polygon))

if __name__ == '__main__':
    unittest.main()