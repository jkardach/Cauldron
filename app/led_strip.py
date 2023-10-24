import abc
from enum import Enum
import numpy as np
from typing import Callable


_RGB_COLOR_SIZE = 3


class PixelOrder(Enum):
    RGB = (0,)
    BGR = 1


class LedStrip(abc.ABC):
    def __del__(self):
        self.fill((0, 0, 0))

    @abc.abstractmethod
    def __setitem__(self, indices, value):
        return None

    @abc.abstractmethod
    def __getitem__(self, indices):
        return None

    @abc.abstractmethod
    def fill(self, color: tuple):
        return None

    @abc.abstractmethod
    def fill_copy(self, pixels: np.array) -> int:
        return 0

    @abc.abstractmethod
    def set_pixel_color(self, index: int, color: tuple):
        return None

    @property
    @abc.abstractmethod
    def brightness(self) -> float:
        return None

    @brightness.setter
    @abc.abstractmethod
    def brightness(self, brightness: float):
        return None

    @abc.abstractmethod
    def num_pixels(self) -> int:
        return 0

    @abc.abstractmethod
    def show(self):
        return None


class RGBArrayStrip(LedStrip):
    def __init__(self, num_pixels: int):
        self._num_pixels = num_pixels
        self._pixels = np.zeros((num_pixels, 3)).astype(np.uint8)
        self._brightness = 1.0

    def __setitem__(self, indices, value):
        self._pixels[indices] = value

    def __getitem__(self, indices):
        return self._pixels[indices]

    def set_show_callback(self, show_callback: Callable[[np.array], None]):
        self._show_callback = show_callback

    def fill(self, color: list):
        assert len(color) == _RGB_COLOR_SIZE
        self._pixels = np.array([color] * self._num_pixels)

    def fill_copy(self, pixels: np.array) -> int:
        assert (
            pixels.shape == self._pixels.shape
        ), f"{pixels.shape} != {self._pixels.shape}"
        self._pixels = pixels.copy()

    def set_pixel_color(self, index: int, color: list):
        assert len(color) == _RGB_COLOR_SIZE
        self._pixels[index] = color

    @property
    def brightness(self) -> float:
        return self._brightness

    @brightness.setter
    def brightness(self, brightness: float):
        self._brightness = brightness

    def get_pixels(self, pixel_order: PixelOrder):
        if pixel_order == PixelOrder.RGB:
            return self._pixels
        elif pixel_order == PixelOrder.BGR:
            return self._pixels[:, [2, 1, 0]]
        raise ValueError("Invalid PixelOrder")

    def num_pixels(self) -> int:
        return self._num_pixels

    def show(self):
        if self._show_callback:
            self._show_callback(self._pixels)


class MockStrip(RGBArrayStrip):
    def __init__(
        self, num_pixels: int, show_callback: Callable[[np.array], None] = None
    ):
        RGBArrayStrip.__init__(self, num_pixels)
        self._show_callback = show_callback

    def get_pixels(self):
        return self._pixels
