import numpy.testing as npt

class TestShapeMixin:
    def assert_pos_equal(self, actual, expected):
        npt.assert_array_equal(actual, expected)

    def assert_pos_almost_equal(self, actual, expected):
        npt.assert_array_almost_equal(actual, expected)
