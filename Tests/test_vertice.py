import unittest
import numpy as np
import numpy.testing as npt
from testPrint import testPrint

from vectorshape.vertice import Vertice


class TestVertice(unittest.TestCase):

    def setUp(self):
        self.coords = (0, 0, 0)
        self.name = "verty"
        self.vert = Vertice(self.coords,self.name)

    def test_vertice_instantiation(self):
        vert = Vertice((1, 2, 3), "instantiation test vertice")
        testPrint(vert)
        npt.assert_array_equal(vert.get_pos(), np.array([1, 2, 3]))

    def test_get_pos(self):
        self.vert.get_pos()
        testPrint(self.vert)
        npt.assert_array_equal(self.vert.get_pos(), np.array(self.coords))

    def test_set_pos(self):
        self.coords = (1, 2, 3)
        self.vert.set_pos(self.coords)
        testPrint(self.vert)
        npt.assert_array_equal(self.vert.get_pos(), np.array(self.coords))

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
