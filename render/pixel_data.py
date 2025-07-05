class PixelData:
    def __init__(self, indices: tuple[int, int], brightness: float, length: float):
        self.indices = tuple(map(int, indices))
        self.brightness = brightness
        self.length = length

    def __repr__(self):
        return f'<{self.__class__.__name__}: [{self.indices[0]},{self.indices[1]}] l={self.length} b={self.brightness}>'

    def set_indices(self, indices: tuple[int, int]):
        self.indices = tuple(map(int, indices))

    def get_indices(self) -> tuple[int, int]:
        return self.indices

    def set_brightness(self, brightness: float):
        self.brightness = brightness

    def get_brightness(self) -> float:
        return self.brightness

    def set_length(self, length: float):
        self.length = length

    def get_length(self) -> float:
        return self.length

