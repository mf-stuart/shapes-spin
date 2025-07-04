import numpy as np
import default_constants as k
from vectorshape.reflection_point import ReflectionPoint
from vectorshape.sensor_rect import SensorRect


class Viewport:

    def __init__(self):
        self.z_buffer = np.full((k.VIEW_HEIGHT, k.VIEW_WIDTH), 0)
        self.frame_plane = SensorRect()

