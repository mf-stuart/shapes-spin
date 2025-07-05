from render.viewport import Viewport
from vectorshape.vertice import Vertice


class Scene():
    def __init__(self):
        self.light_box = Vertice((10, 10, 10), "LightBox")
        self.render_window = Viewport()

    def setup(self):
        pass

    def render_frame(self):
        pass