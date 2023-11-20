import abc
import led_effect
import led_strip
import players
from pydub import AudioSegment
from random import choice
import threading


BUBBLE_LENGTHS = [7, 9, 11]
BUBBLE_POP_SPEEDS = [3000, 4000, 5000]
BUBBLE_PROB_WEIGHTS = [0.5, 0.25, 0.25]
BUBBLE_SPAWN_PROB = 0.05
BUBBLING_SOUND = "app/files/audio/bubbles.wav"
CAULDRON_COLORS = [
    ([32, 139, 25], [215, 232, 23]),
    ([142, 75, 166], [237, 114, 178]),
    ([255, 179, 0], [255, 0, 60]),
    ([235, 57, 21], [76, 172, 194]),
]
EXPLOSION_SOUND = "app/files/audio/poof.wav"
MAX_BUBBLES = 10


class ICauldron(abc.ABC):
    """Interface to control the Cauldron."""

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def is_playing(self):
        pass

    @abc.abstractmethod
    def cause_explosion(self):
        """Causes the Cauldron to explode, changing the color."""
        return None


class Cauldron(ICauldron):
    """Cauldron implementation."""

    def __init__(self, strip: led_strip.LedStrip):
        self._lock = threading.Lock()
        self._strip = strip

        # Initialize color possibilities
        self._colors = CAULDRON_COLORS
        self._current_color_index = 0
        self._current_colors = self._colors[self._current_color_index]

        # Initialize bubbling effects players
        self._current_bubbling_effect = None
        self._bubbling_handle: players.Handle = None
        self._init_bubbling_effects()
        segment = AudioSegment.from_file(BUBBLING_SOUND)
        segment.frame_rate = int(segment.frame_rate / 4)
        self._bubbling_audio_player = players.AudioPlayer(segment)

        # Initialize explosion effects
        self._current_explosion_effect = None
        self._explosion_handle: players.Handle = None
        self._init_explosion_effects()

        # Start the common effect
        self._bubbling_audio_handle = None
        self.start()

    def __del__(self):
        self.stop()

    def start(self):
        if (
            self._bubbling_audio_handle is not None
            or self._bubbling_handle is not None
        ):
            return
        self._bubbling_audio_handle = self._bubbling_audio_player.loop()
        self._start_common_effect()

    def stop(self):
        self._strip.fill((0, 0, 0))
        self._strip.show()
        if self._explosion_handle:
            self._explosion_handle.stop_wait()
            self._explosion_handle = None
        if self._bubbling_handle:
            self._bubbling_handle.stop_wait()
            self._bubbling_handle = None
        if self._bubbling_audio_handle:
            self._bubbling_audio_handle.stop_wait()
            self._bubbling_audio_handle = None

    def is_playing(self):
        return (
            self._bubbling_audio_handle.is_playing()
            and self._bubbling_handle.is_playing()
        )

    def _init_explosion_effects(self):
        segment = AudioSegment.from_file(EXPLOSION_SOUND)
        segment = segment.set_sample_width(2)
        segment += 30
        explosion_audio = players.AudioPlayer(segment)

        self._current_explosion_effect = led_effect.AudioToBrightnessEffect(
            self._strip, segment, frame_speed_ms=33
        )
        explosion_effect_player = players.LedEffectPlayer(
            self._current_explosion_effect
        )
        self._explosion_av = players.AudioVisualPlayer(
            explosion_effect_player, explosion_audio
        )
        self._explosion_handle = None

    def _init_bubbling_effects(self):
        self._bubbling_effects: list[players.LedEffectPlayer] = []
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
                frame_speed_ms=33,
            )
            bubbling_effect_player = players.LedEffectPlayer(bubbling_effect)
            self._bubbling_effects.append(bubbling_effect_player)
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
            self._strip.fill(self._current_colors[0])
            self._bubbling_handle = self._current_bubbling_effect.loop()

    def cause_explosion(self):
        """Causing an explosion will change the color and strobe the lights."""
        if self._explosion_handle is not None:
            self._explosion_handle.stop_wait()
        self._current_explosion_effect.reset()
        self._set_random_colors()
        self._explosion_handle = self._explosion_av.play()
