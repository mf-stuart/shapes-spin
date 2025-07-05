import unittest
import numpy as np
import numpy.testing as npt
from tools import testPrint, numpify_3vector

from vectorshape.vertice import Vertice

class TestVertice(unittest.TestCase):

    def setUp(self):
        self.coords = (0, 0, 0)
        self.name = "verty"
        self.vert = Vertice(self.coords,self.name)

    def test_vertice_instantiation(self):
        pos = (1, 2 ,3)
        name = "instantiation test vertice"
        vert = Vertice(pos, name)
        testPrint(vert)
        npt.assert_array_equal(vert.get_pos(), numpify_3vector(pos))
        self.assertEqual(vert.get_name(), name)

    def test_instantiation_invalid_length(self):
        with self.assertRaises(ValueError):
            Vertice((1, 2), "bad vertice")

        with self.assertRaises(ValueError):
            Vertice((1, 2, 3, 4), "bad vertice")

    def test_instantiation_invalid_type(self):
        with self.assertRaises(TypeError):
            Vertice(("a", "b", "c"), "bad vertice")

    def test_get_pos(self):
        self.vert.get_pos()
        testPrint(self.vert)
        npt.assert_array_equal(self.vert.get_pos(), np.array(self.coords))

    def test_set_pos(self):
        self.coords = (1, 2, 3)
        self.vert.set_pos(self.coords)
        testPrint(self.vert)
        npt.assert_array_equal(self.vert.get_pos(), np.array(self.coords))

    def test_set_pos_invalid_length(self):
        vert = Vertice((0, 0, 0), "bad vertice")
        with self.assertRaises(ValueError):
            vert.set_pos((1, 2))

        with self.assertRaises(ValueError):
            vert.set_pos((1, 2, 3, 4))

    def test_set_pos_invalid_type(self):
        vert = Vertice((0, 0, 0), "bad vertice")
        with self.assertRaises(TypeError):
            vert.set_pos(("x", "y", "z"))

    def test_get_name(self):
        name = self.vert.get_name()
        testPrint(name)
        self.assertEqual(name, self.name)

    def test_set_name(self):
        new_name = "verty jr"
        self.vert.set_name(new_name)
        testPrint(self.vert)
        self.assertEqual(self.vert.get_name(), new_name)


if __name__ == '__main__':
    unittest.main()
