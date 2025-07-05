import unittest
import numpy as np

import default_constants as k
from unittest.mock import patch
from render.viewport import Viewport
from render.pixel_data import PixelData

class TestViewport(unittest.TestCase):
    def setUp(self):
        self.viewport = Viewport()
        self.viewport.flush()

    def test_flush_resets_screen_and_buffer(self):
        self.viewport.screen[0, 0] = 'X'
        self.viewport.inverse_z_buffer[0, 0] = 100
        self.viewport.flush()
        self.assertTrue(np.all(self.viewport.screen == ' '))
        self.assertTrue(np.all(self.viewport.inverse_z_buffer == 0))

    def test_compare_to_buffer_true_false(self):
        self.viewport.inverse_z_buffer[0, 0] = 1 / 5
        self.assertFalse(self.viewport.compare_to_buffer(0, 0, 10))
        self.assertTrue(self.viewport.compare_to_buffer(0, 0, 3))

    def test_process_pixels_updates_screen_and_buffer(self):
        pixels = [
            PixelData((1, 2), 0.5, 5),
            PixelData((3, 4), 0.9, 2),
            PixelData((1, 2), 0.1, 3),
        ]

        self.viewport.process_pixels(pixels)

        self.assertAlmostEqual(self.viewport.inverse_z_buffer[2, 1], 1 / 3)
        self.assertAlmostEqual(self.viewport.inverse_z_buffer[4, 3], 1 / 2)

        char_1 = self.viewport.get_char_from_brightness(0.1)
        char_2 = self.viewport.get_char_from_brightness(0.9)
        self.assertEqual(self.viewport.screen[2, 1], char_1)
        self.assertEqual(self.viewport.screen[4, 3], char_2)

    @patch('render.viewport.clear_console')
    def test_printout_pixels_calls_clear_console_and_prints(self, mock_clear_console):
        pixels = [
            PixelData((0, 0), 1, 0.5),
            PixelData((1, 1), 1, 0.5),
        ]
        self.viewport.process_pixels(pixels)

        with patch('builtins.print') as mock_print:
            self.viewport.printout_pixels()
            mock_clear_console.assert_called_once()
            self.assertEqual(mock_print.call_count, k.VIEW_HEIGHT)

if __name__ == '__main__':
    unittest.main()
