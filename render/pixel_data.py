class PixelData:
    def __init__(self, indices: tuple[int, int], brightness: float, length: float):
        self.indices = indices
        self.brightness = brightness
        self.length = length

    def set_indices(self, indices: tuple[int, int]):
        self.indices = indices

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

