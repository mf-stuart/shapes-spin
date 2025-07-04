import numpy as np

import default_constants as k
from test_polygon import TestPolygon


class TestScreenRect(TestPolygon):

    @override
    def test_generate_orthogonal_basis(self):
        self.shape.generate_plane()
        u, v = self.shape.generate_orthogonal_basis()
        dot_product = np.dot(u, v)
        self.assertAlmostEqual(dot_product, 0.0, delta=1e-6)
        self.assertAlmostEqual(np.linalg.norm(u), k.PIXEL_SIZE, delta=1e-6)
        self.assertAlmostEqual(np.linalg.norm(v), k.PIXEL_SIZE, delta=1e-6)
