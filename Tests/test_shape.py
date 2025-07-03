import unittest
import numpy as np
import numpy.testing as npt
from tools import testPrint, numpify_3vector, normpify_3vector
from vectorshape.shape import Shape

class TestShape(unittest.TestCase):

    def setUp(self):
        self.pos_instantiate = (0.0, 0.0, 0.0)
        self.name = "shapeson"
        self.shape = Shape(self.pos_instantiate, self.name)

    def test_shape_instantiation(self):
        pos = (1, 2, 3)
        name = "instantiation test shape"
        shape = Shape(pos, name)
        testPrint(shape)
        npt.assert_array_equal(shape.get_pos(), numpify_3vector(pos))
        self.assertEqual(shape.get_name(), name)

    def test_instantiation_invalid_pos_length(self):
        with self.assertRaises(ValueError):
            Shape((1, 2),"bad shape")

        with self.assertRaises(ValueError):
            Shape((1, 2, 3, 4),"bad shape")

    def test_get_pos(self):
        npt.assert_array_equal(self.shape.get_pos(), np.array(self.pos_instantiate))

    def test_set_pos(self):
        new_pos = (5, 6, 7)
        self.shape.set_pos(new_pos)
        testPrint(self.shape)
        npt.assert_array_equal(self.shape.get_pos(), np.array(new_pos))

    def test_set_pos_invalid_length(self):
        with self.assertRaises(ValueError):
            self.shape.set_pos((1, 2))

        with self.assertRaises(ValueError):
            self.shape.set_pos((1, 2, 3, 4))

if __name__ == '__main__':
    unittest.main()
