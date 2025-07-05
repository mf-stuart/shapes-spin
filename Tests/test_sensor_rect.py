import unittest
import numpy as np

import default_constants as k
from vectorshape.sensor_rect import SensorRect
from vectorshape.reflection_point import ReflectionPoint
from test_shape_mixin import TestShapeMixin

class TestSensorRect(unittest.TestCase, TestShapeMixin):

    def setUp(self):
        self.sensor_rect = SensorRect()

    def test_open_shutter_returns_expected_pixel_data(self):
        reflection = ReflectionPoint((10.0, 5.0, 30.0), 0.8, "bright")
        camera_pos = self.sensor_rect.camera_pos
        result = self.sensor_rect.open_shutter([reflection])
        self.assertEqual(len(result), 1)
        pixel = result[0]
        self.assertEqual(len(pixel.get_indices()), 2)
        self.assertGreater(pixel.get_length(), 0)
        self.assertEqual(pixel.get_brightness(), 0.8)

    def test_open_shutter_ignores_no_intersection(self):
        self.sensor_rect.normal = np.array([0.0, 1.0, 0.0])
        reflection = ReflectionPoint((10.0, -5.0, 50.0), 1.0, "dark")
        result = self.sensor_rect.open_shutter([reflection])
        self.assertEqual(result, [])

    def test_repr_outputs_expected_format(self):
        expected_start = f'<SensorRect "{self.sensor_rect.get_name()}": at ['
        repr_str = repr(self.sensor_rect)
        self.assertTrue(repr_str.startswith(expected_start))
        self.assertIn("facing", repr_str)
        self.assertIn("with [TL,TR,BR,BL]", repr_str)

    def test_generate_plane_sets_correct_normal_and_plane_eq(self):
        self.sensor_rect.generate_plane()
        self.assertIsNotNone(self.sensor_rect.get_normal())
        self.assertIsNotNone(self.sensor_rect.plane_eq)
        normal = self.sensor_rect.get_normal()
        self.assertAlmostEqual(np.linalg.norm(normal), 1.0, delta=k.EPSILON)

    def test_generate_orthogonal_basis_returns_orthonormal_vectors(self):
        u, v = self.sensor_rect.generate_orthogonal_basis()
        dot_product = np.dot(u, v)
        self.assertAlmostEqual(dot_product, 0.0, delta=k.EPSILON)
        self.assertAlmostEqual(np.linalg.norm(u), 1, delta=k.EPSILON)
        self.assertAlmostEqual(np.linalg.norm(v), 1, delta=k.EPSILON)

    def test_get_pos_and_set_pos_update_position_and_vertices(self):
        old_pos = self.sensor_rect.get_pos().copy()
        old_vertices_pos = [v.get_pos().copy() for v in self.sensor_rect.get_vertices()]
        new_pos = old_pos + np.array([1.0, 1.0, 1.0])
        self.sensor_rect.set_pos(tuple(new_pos))
        np.testing.assert_array_almost_equal(self.sensor_rect.get_pos(), new_pos)

        for vertex, old_vertice_pos in zip(self.sensor_rect.get_vertices(), old_vertices_pos):
            self.assertTrue(np.linalg.norm(vertex.get_pos() - old_vertice_pos) > 0)

    def test_shift_position_moves_all_vertices_correctly(self):
        old_positions = [v.get_pos().copy() for v in self.sensor_rect.get_vertices()]
        movement = (1.0, 2.0, 3.0)
        self.sensor_rect.shift_position(movement)
        for old, vert in zip(old_positions, self.sensor_rect.get_vertices()):
            expected_new = old + np.array(movement)
            np.testing.assert_array_almost_equal(vert.get_pos(), expected_new)

    def test_coplanar_position_by_basis_returns_valid_indices(self):

        point = self.sensor_rect.get_vertices()[0].get_pos()
        indices = self.sensor_rect.find_pixel_coordinate_from_projection(point)
        self.assertIsInstance(indices, tuple)
        self.assertEqual(len(indices), 2)
        self.assertTrue(all(isinstance(i, float) for i in indices))

if __name__ == '__main__':
    unittest.main()