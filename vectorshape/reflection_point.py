from typing import override

from vectorshape.vertice import Vertice


class ReflectionPoint(Vertice):

    def __init__(self, pos_arr: tuple[float, float, float], brightness: float, name: str):
        super().__init__(pos_arr, name)
        self.brightness: float = brightness

    @override
    def __repr__(self):
        return f"<ReflectionPoint {self.name} at [{self.pos[0]},{self.pos[1]},{self.pos[2]}] b={self.brightness}>"

    def set_brightness(self, brightness: float):
        self.brightness = brightness

    def get_brightness(self) -> float:
        return self.brightness