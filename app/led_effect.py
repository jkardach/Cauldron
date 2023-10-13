import abc
from led_strip import LedStrip
import numpy as np
from numpy.random import choice
from pydub import AudioSegment
import random
import threading


TWO_PI = np.pi * 2


class LedEffect(abc.ABC):
    def __init__(self):
        self.frame_speed_ms = 50

    @abc.abstractmethod
    def apply_effect(self, strip: LedStrip):
        return None


class SineWaveEffect(LedEffect):
    """Applies a modifyable sine wave effect onto an LedStrip."""

    def __init__(
        self,
        color0: list,
        color1: list,
        b: float = 1,
        oscillate: bool = False,
        oscillation_speed_ms: int = 250,
    ):
        assert len(color0) == len(color1)
        LedEffect.__init__(self)
        self._lock = threading.Lock()
        # Convert colors to numpy arrays
        self._color0 = np.array(color0)
        self._color1 = np.array(color1)
        self.oscillation_speed_ms = oscillation_speed_ms
        self._oscillate = oscillate
        self.wave_length = b

        # Offset the wave so that each color is above or equal to 0
        self._y_offsets = np.abs(
            (self._color0 - self._color1) / 2
        ) + np.minimum(self._color0, self._color1)
        # Keep track of the current amplitude value
        self._amplitudes = np.array([(self._color0 - self._color1) / 2])
        self._current_a = self._amplitudes.copy()
        # Compute how much the amplitude should change between each frame
        self._amplitude_inc = (2 * np.pi) / self._oscillation_inc
        self._amplitude_x = 0

    def _update_pixel_values_locked(self, x: np.array) -> np.array:
        """Returns the brightness value (y-value) of the sine wave.

        The sine wave equation is as follows:

        y = new color value
        x = x value for LED
        a = amplitude
        b = wave length
        y_offset = y offset

        y = a * sin(b * x) + y_offset

        If oscillation is on, the value of 'a' will range from "-a -> a" then
        "a -> -a" continuously.
        """
        assert self._lock.locked()
        pixels = np.zeros((len(x), len(self._current_a)))
        pixels = np.cos(self._b * x).T * self._current_a + self._y_offsets
        return pixels

    def _update_oscillation_locked(self):
        """Updates the sine wave variables if oscillation is on.

        Oscillation will cause the amplitude of the sine wave to range between
        "a -> -a" then "-a -> a" continuously.
        """
        assert self._lock.locked()
        if not self._oscillate:
            return
        self._amplitude_x += self._amplitude_inc
        self._current_a = self._amplitudes * np.cos(self._amplitude_x)

    def apply_effect(self, strip: LedStrip):
        """Applies the sine wave effect onto the LedStrip."""
        num_pixels = strip.num_pixels()
        x_values = np.array([np.arange(0, TWO_PI, TWO_PI / num_pixels)])
        with self._lock:
            pixels = self._update_pixel_values_locked(x_values)
            strip.fill_copy(pixels)
            self._update_oscillation_locked()

        strip.show()

    @property
    def wave_length(self) -> float:
        return self._b

    @wave_length.setter
    def wave_length(self, b: float):
        with self._lock:
            self._b = b

    @property
    def oscillate(self) -> bool:
        return self._oscillate

    @oscillate.setter
    def oscillate(self, enable: bool):
        with self._lock:
            self.oscillate = enable

    @property
    def oscillation_speed_ms(self) -> int:
        return self._oscillation_speed_ms

    @oscillation_speed_ms.setter
    def oscillation_speed_ms(self, speed_ms: int):
        with self._lock:
            self._oscillation_speed_ms = speed_ms
            self._oscillation_inc = speed_ms / self.frame_speed_ms


class BubbleEffect(LedEffect):
    def __init__(
        self,
        bubble_index: int,
        base_color: list,
        bubble_color: list,
        bubble_length: int = 5,
        bubble_pop_speed_ms: int = 3000,
    ):
        assert bubble_index >= 0
        LedEffect.__init__(self)
        self._bubble_index = bubble_index - int(bubble_length / 2)
        self._base_color = np.array([base_color])
        self._bubble_color = np.array([bubble_color])
        self._bubble_pop_speed_ms = bubble_pop_speed_ms
        self._bubble_length = bubble_length
        # Calculate number of frames it will take for the animation to complete
        self._pop_increments = int(
            self._bubble_pop_speed_ms / self.frame_speed_ms
        )
        self._current_increment = 0
        # Calculate bubble y value amplitude increments
        x_values = self._get_x_values(self._pop_increments)
        self._y_increments = np.array((np.cos(x_values + np.pi) + 1) / 2)
        # Calculate bubble max amplitude
        self._bubble_amplitude = self._bubble_color - self._base_color

    def _get_x_values(self, length: int) -> np.array:
        x_inc = TWO_PI / (length - 1)
        return np.arange(0, TWO_PI + x_inc, x_inc)

    def apply_effect(self, strip: LedStrip):
        """Applies a bubble to the LedStrip."""
        num_pixels = strip.num_pixels()
        # Calculate x values of the bubble
        assert self._bubble_index < num_pixels
        max_index = min(
            num_pixels - 1, self._bubble_index + self._bubble_length
        )
        bubble_x_values = np.arange(self._bubble_index, max_index, 1)
        x_values = np.array([self._get_x_values(len(bubble_x_values))])
        # Calculate the y values of the current bubble increment
        amp_fact = self._y_increments[
            self._current_increment % self._pop_increments
        ]
        amplitude = amp_fact * self._bubble_amplitude
        colors = (
            np.array((np.cos(x_values + np.pi) + 1).T * amplitude)
            + self._base_color
        )
        colors = np.clip(colors, 0, 255)
        strip[bubble_x_values] = colors
        self._current_increment += 1
        strip.show()


class BubblingEffect(LedEffect):
    def __init__(
        self,
        base_color: list,
        bubble_color: list,
        bubble_lengths: list,
        bubble_length_weights: list,
        bubble_pop_speeds_ms: list,
        bubble_pop_speed_weights: list,
        max_bubbles: int,
        bubble_spawn_prob: float,
    ):
        LedEffect.__init__(self)
        assert len(bubble_lengths) == len(bubble_length_weights)
        assert len(bubble_pop_speeds_ms) == len(bubble_pop_speed_weights)
        assert bubble_spawn_prob > 0 and bubble_spawn_prob <= 1
        self._base_color = np.array([base_color])
        self._bubble_color = np.array([bubble_color])
        self._max_bubbles = max_bubbles
        self._bubble_spawn_prob = bubble_spawn_prob
        self._bubble_lengths = bubble_lengths
        self._bubble_length_weights = bubble_length_weights
        self._bubble_pop_speeds = bubble_pop_speeds_ms
        self._bubble_pop_speed_weights = bubble_pop_speed_weights
        self._current_bubbles: dict[int, BubbleEffect] = {}

    def _spawn_bubble(self):
        return random.random() <= self._bubble_spawn_prob

    def apply_effect(self, strip: LedStrip):
        """Applies a bubble to the LedStrip."""
        spawn_bubble = self._spawn_bubble()
        num_pixels = strip.num_pixels()
        if spawn_bubble and len(self._current_bubbles) < self._max_bubbles:
            bubble_index = random.randint(0, num_pixels - 1)
            while bubble_index in self._current_bubbles:
                bubble_index = random.randint(0, num_pixels - 1)
            bubble_length = choice(
                self._bubble_lengths, 1, p=self._bubble_length_weights
            )[0]
            bubble_pop_speed_ms = choice(
                self._bubble_pop_speeds, 1, p=self._bubble_pop_speed_weights
            )[0]
            bubble_effect = BubbleEffect(
                bubble_index,
                self._base_color,
                self._bubble_color,
                bubble_length,
                bubble_pop_speed_ms,
            )
            self._current_bubbles[bubble_index] = bubble_effect
        for bubbles in self._current_bubbles.values():
            bubbles.apply_effect(strip)
        strip.show()


class AudioToBrightnessEffect(LedEffect):
    """Changes the brightness of the LedStrip based on AudioSegment volume."""

    def __init__(self, segment: AudioSegment):
        LedEffect.__init__(self)
        data = np.array(segment.get_array_of_samples())
        data = np.abs(data.astype(np.int32))
        self._normalized_data = (data - np.min(data)) / (
            np.max(data) - np.min(data)
        )
        self._duration_s = segment.duration_seconds
        self._current_iteration = 0
        self._total_increments = int(
            segment.duration_seconds * 1000 / self.frame_speed_ms
        )
        self._iteration_increment = int(
            len(self._normalized_data) / self._total_increments
        )
        self._starting_brightness = None
        self._timestamp_ms = 0

    def apply_effect(self, strip: LedStrip):
        """Applies a bubble to the LedStrip."""
        self._timestamp_ms += self.frame_speed_ms
        if self._starting_brightness is None:
            self._starting_brightness = strip.brightness
        brightness = self._normalized_data[self._current_iteration]
        strip.brightness = brightness
        self._current_iteration += self._iteration_increment
        if self._current_iteration > len(self._normalized_data):
            strip.brightness = self._starting_brightness
            self._current_iteration = 0
        strip.show()
