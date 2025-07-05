import sys
import numpy as np

import default_constants as k
from render.pixel_data import PixelData
from tools import bucketize, clear_console
from vectorshape.sensor_rect import SensorRect


class Viewport:

    def __init__(self):
        self.screen = np.full((k.VIEW_HEIGHT, k.VIEW_WIDTH), ' ')
        self.inverse_z_buffer = np.full((k.VIEW_HEIGHT, k.VIEW_WIDTH), 0,  dtype=np.float32)
        self.frame_plane = SensorRect()

    def flush(self):
        self.screen = np.full((k.VIEW_HEIGHT, k.VIEW_WIDTH), ' ')
        self.inverse_z_buffer = np.full((k.VIEW_HEIGHT, k.VIEW_WIDTH), 0,  dtype=np.float32)

    def get_char_from_brightness(self, brightness):
        no_buckets = len(k.PIXEL_TYPES)
        index = bucketize(brightness, no_buckets)
        return k.PIXEL_TYPES[index]


    def compare_to_buffer(self, y: int, x: int, length: float) -> bool:
        try:
            return bool((1 / length) > self.inverse_z_buffer[y, x])
        except IndexError:
            return False

    def process_pixels(self, pixels: list[PixelData]):
        self.flush()
        for pixel in pixels:
            x, y = pixel.get_indices()
            try:
                if self.compare_to_buffer(y, x, pixel.get_length()):
                    self.inverse_z_buffer[y, x] = 1 / pixel.get_length()
                    self.screen[y, x] = self.get_char_from_brightness(pixel.get_brightness())
            except IndexError:
                continue

    def printout_pixels(self):
        clear_console()
        for y in range(k.VIEW_HEIGHT):
            line_pixels = []
            for x in range(k.VIEW_WIDTH):
                pixel = self.screen[y, x]
                line_pixels.append(pixel)
            print(''.join(line_pixels), flush=True)

