import numpy as np
import default_constants as k


class Viewport:

    def __init__(self):
        self.z_buffer = np.full((k.VIEW_HEIGHT, k.VIEW_WIDTH), np.inf)
        self.plane_frame = 0