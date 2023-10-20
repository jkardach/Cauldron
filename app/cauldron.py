import board
import led_effect
import led_strip
import neopixel
from neopixel_strip import NeoPixelStrip
import players
from pydub import AudioSegment
from random import choice
import threading
import time

PIXEL_ORDER = neopixel.RGB
PIXEL_PIN = board.D18
NUM_PIXELS = 50

BUBBLE_LENGTHS = [7, 9, 11]
BUBBLE_POP_SPEEDS = [3000, 4000, 5000]
BUBBLE_PROB_WEIGHTS = [0.5, 0.25, 0.25]
MAX_BUBBLES = 10
BUBBLE_SPAWN_PROB = 0.05
EXPLOSION_SOUND = "app/files/audio/poof.wav"
BUBBLING_SOUND = "app/files/audio/bubbles.wav"


class Cauldron:
    def __init__(self, strip: led_strip.LedStrip):
        self._lock = threading.Lock()
        self._strip = strip

        # Initialize color possibilities
        self._colors = [
            ([32, 139, 25], [43, 199, 32]),
            ([142, 75, 166], [196, 119, 223]),
            ([255, 179, 0], [255, 222, 0]),
        ]
        self._current_color_index = 0
        self._current_colors = self._colors[self._current_color_index]

        # Initialize bubbling effects players
        self._current_bubbling_effect = None
        self._bubbling_handle: players.Handle = None
        self._init_bubbling_effects()

        # Initialize explosion effects
        self._current_explosion_effect = None
        self._explosion_handle: players.Handle = None
        self._init_explosion_effects()

        # Start the common effect
        self._start_common_effect()

    def __del__(self):
        if self._explosion_handle:
            self._explosion_handle.stop_wait()
        if self._bubbling_handle:
            self._bubbling_handle.stop_wait()

    def _init_explosion_effects(self):
        segment = AudioSegment.from_file(EXPLOSION_SOUND)
        segment = segment.set_sample_width(2)

        self._current_explosion_effect = led_effect.AudioToBrightnessEffect(
            self._strip, segment
        )
        explosion_effect_player = players.LedEffectPlayer(
            self._current_explosion_effect
        )
        explosion_audio = players.AudioPlayer(segment)
        self._explosion_av = players.AudioVisualPlayer(
            explosion_effect_player, explosion_audio
        )
        self._explosion_handle = None

    def _init_bubbling_effects(self):
        self._bubbling_effects: list[players.AudioVisualPlayer] = []
        for colors in self._colors:
            bubbling_effect = led_effect.BubblingEffect(
                self._strip,
                colors[0],
                colors[1],
                BUBBLE_LENGTHS,
                BUBBLE_PROB_WEIGHTS,
                BUBBLE_POP_SPEEDS,
                BUBBLE_PROB_WEIGHTS,
                MAX_BUBBLES,
                BUBBLE_SPAWN_PROB,
            )
            bubbling_effect_player = players.LedEffectPlayer(bubbling_effect)
            segment = AudioSegment.from_file(BUBBLING_SOUND)
            segment.frame_rate = int(segment.frame_rate / 4)
            bubbling_audio_player = players.AudioPlayer(segment)

            bubbling_av = players.AudioVisualPlayer(
                bubbling_effect_player, bubbling_audio_player
            )
            self._bubbling_effects.append(bubbling_av)
        self._current_bubbling_effect = self._bubbling_effects[
            self._current_color_index
        ]
        self._bubbling_handle = None

    def _set_random_colors(self):
        """Selects a new set of colors and applies it to the LedStrip."""
        with self._lock:
            self._current_color_index = choice(
                [
                    i
                    for i in range(0, len(self._colors))
                    if i != self._current_color_index
                ]
            )
            self._current_colors = self._colors[self._current_color_index]
            self._current_bubbling_effect = self._bubbling_effects[
                self._current_color_index
            ]
        self._start_common_effect()

    def _start_common_effect(self):
        """Starts the looping cauldron bubbling effect."""
        if self._bubbling_handle is not None:
            self._bubbling_handle.stop_wait()
        with self._lock:
            bubbling_effect = self._bubbling_effects[self._current_color_index]
            self._strip.fill(self._current_colors[0])
            self._bubbling_handle = bubbling_effect.loop()

    def cause_explosion(self):
        """Causing an explosion will change the color and strobe the lights."""
        if self._explosion_handle is not None:
            self._explosion_handle.stop_wait()
        self._current_explosion_effect.reset()
        self._set_random_colors()
        self._explosion_handle = self._explosion_av.play()


import board
import led_effect
import led_strip
import neopixel
from neopixel_strip import NeoPixelStrip
import players
from pydub import AudioSegment
from random import choice
import threading
import time

import neopixel
import board
from neopixel_strip import NeoPixelStrip

PIXEL_ORDER = neopixel.RGB
PIXEL_PIN = board.D12
NUM_PIXELS = 50
device = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    auto_write=True,
    pixel_order=PIXEL_ORDER,
    brightness=0.1,
)
strip = NeoPixelStrip(device)


def run_cauldron():
    cauldron = Cauldron(strip)

    for i in range(1):
        time.sleep(5)
        print("Causing explosion")
        cauldron.cause_explosion()

    time.sleep(1)


run_cauldron()
