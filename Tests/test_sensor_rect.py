import unittest
import numpy as np
from vectorshape.sensor_rect import SensorRect
from vectorshape.reflection_point import ReflectionPoint
from test_shape_mixin import TestShapeMixin

class TestSensorRect(unittest.TestCase, TestShapeMixin):

    def setUp(self):
        self.shape = SensorRect()

    def test_open_shutter_returns_expected_pixel_data(self):
        reflection = ReflectionPoint((10.0, 5.0, 30.0), 0.8, "bright")
        result = self.shape.open_shutter([reflection])
        self.assertEqual(len(result), 1)
        pixel = result[0]
        self.assertEqual(len(pixel.get_indices()), 2)
        self.assertGreater(pixel.get_length(), 0)
        self.assertEqual(pixel.get_brightness(), 0.8)

    def test_open_shutter_ignores_no_intersection(self):
        self.shape.normal = np.array([0.0, 1.0, 0.0])
        reflection = ReflectionPoint((10.0, -5.0, 50.0), 1.0, "dark")
        result = self.shape.open_shutter([reflection])
        self.assertEqual(result, [])