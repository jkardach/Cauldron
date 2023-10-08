import abc
from led_strip import LedStrip
from led_effect import LedEffect
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import simpleaudio as sa
import threading
import time


class Handle(abc.ABC):
    """The Handle class can stop a Player's asynchronous play/loop action."""

    def __init__(self, player: "Player"):
        self._player = player

    def __del__(self):
        self._player.stop()

    def stop(self):
        self._player.stop()


class Player(abc.ABC):
    """A Player asynchronously plays/loops an action on another thread."""

    def __init__(self):
        self._handle = None
        self._lock = threading.Lock()

    @abc.abstractmethod
    def _play(self):
        return None

    @abc.abstractmethod
    def _loop(self):
        return None

    def play(self) -> Handle:
        """Runs _play on another thread, returning a Handle to the thread."""
        with self._lock:
            if self._handle:
                return self._handle
            threading.Thread(target=self._play).start()
            self._handle = Handle(self)
            return self._handle

    def loop(self) -> Handle:
        """Runs _loop on another thread, returning a Handle to the thread."""
        with self._lock:
            if self._handle:
                return self._handle
            threading.Thread(target=self._loop).start()
            self._handle = Handle(self)
            return self._handle

    @abc.abstractmethod
    def stop(self):
        return None


class LedEffectPlayer(Player):
    """Plays an LedEffect on an LedStrip."""

    def __init__(self, strip: LedStrip, effect: LedEffect):
        Player.__init__(self)
        self._strip = strip
        self._effect = effect
        self._play_effect = False

    def _loop(self):
        with self._lock:
            self._play_effect = True
        while self._play_effect:
            self._effect.apply_effect(self._strip)
            time.sleep(self._effect.frame_speed_ms / 1000.0)

    def _play(self):
        self._loop()

    def stop(self):
        with self._lock:
            self._play_effect = False


class AudioPlayer(Player):
    """Plays an AudioSegment."""

    def __init__(self, seg: AudioSegment):
        Player.__init__(self)
        self._sound = seg
        self._play_buffer = None
        self._play_audio = False

    def _create_play_buffer(self, seg) -> sa.PlayObject:
        return sa.play_buffer(
            seg.raw_data,
            num_channels=seg.channels,
            bytes_per_sample=seg.sample_width,
            sample_rate=seg.frame_rate,
        )

    def _loop(self):
        with self._lock:
            self._play_audio = True
        while self._play_audio:
            with self._lock:
                self._play_buffer = self._create_play_buffer(self._sound * 10)
            self._play_buffer.wait_done()

    def _play(self):
        with self._lock:
            self._play_buffer = self._create_play_buffer(self._sound)
        self._play_buffer.wait_done()

    def stop(self):
        with self._lock:
            self._play_audio = False
            if self._play_buffer:
                self._play_buffer.stop()


class AudioVisualPlayer(Player):
    """Plays both audio and LED visuals simultaneously."""

    def __init__(
        self, effect_player: LedEffectPlayer, audio_player: AudioPlayer
    ):
        Player.__init__(self)
        self._effect_player = effect_player
        self._audio_player = audio_player
        self._playing = False
        self._effect_handle = None
        self._audio_handle = None
        self._condition = threading.Condition()

    def _loop(self):
        with self._condition:
            self._audio_handle = self._audio_player.loop()
            self._effect_handle = self._effect_player.play()
            self._condition.wait()

    def _play(self):
        with self._condition:
            self._audio_handle = self._audio_player.play()
            self._effect_handle = self._effect_player.play()
            self._condition.wait()

    def stop(self):
        if self._handle is None:
            return None
        self._effect_handle.stop()
        self._audio_handle.stop()
        self._condition.notify()


class MockAudioVisualPlayer(AudioVisualPlayer):
    def __init__(
        self, effect_player: LedEffectPlayer, audio_player: AudioPlayer
    ):
        AudioVisualPlayer.__init__(self, effect_player, audio_player)

    def play(self):
        self._play()

    def loop(self):
        self._loop()


class MockEffectPlayer(Player):
    def __init__(self, strip: LedStrip, effect: LedEffect):
        self._strip = strip
        self._effect = effect

    def _loop(self):
        fig, ax = plt.subplots()
        num_pixels = self._strip.num_pixels()
        x = np.arange(0, num_pixels, 1)
        y = [3] * num_pixels
        ax.set(xlim=[0, num_pixels], ylim=[0, 6])
        # Create scatter plot to simulate LEDs
        scat = plt.scatter(x, y, s=50)

        # Create set_pixels callback to change the LED scatter plot dot colors
        def set_pixels(pixels: np.array):
            scat.set_color(pixels / 255.0)

        # Set the show callback to update the pixel colors. This will call
        # set_pixels when LedStrip.show is called.
        self._strip.set_show_callback(set_pixels)

        # Create the pyplot animation update method. This will update the
        # LedStrip pixels
        def update(_):
            self._effect.apply_effect(self._strip)
            return scat

        ani = animation.FuncAnimation(
            fig=fig,
            func=update,
            frames=40,
            interval=self._effect.frame_speed_ms,
        )
        plt.show()
        return Handle(self)

    def _play(self):
        self._loop()

    def play(self):
        self._loop()

    def loop(self):
        self._loop()

    def stop(self):
        return None
