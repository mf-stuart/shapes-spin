from vectorshape.vertice import Vertice


class ReflectionPoint(Vertice):

    def __init__(self, pos_arr: tuple[float, float, float], brightness: float, name: str):
        super().__init__(pos_arr, name)
        self.brightness: float = brightness

    def set_brightness(self, brightness: float):
        self.brightness = brightness

    def get_brightness(self) -> float:
        return self.brightness