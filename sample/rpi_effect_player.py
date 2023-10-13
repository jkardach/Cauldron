import board
import led_effect
from neopixel_strip import NeoPixelStrip
import neopixel
import players
from pydub import AudioSegment
import time


PIXEL_ORDER = neopixel.RGB
PIXEL_PIN = board.D18
NUM_PIXELS = 50


def test_rpi_neopixel_sine_wave():
    color0 = [3, 252, 11]
    color1 = [229, 245, 5]

    sine_wave = led_effect.SineWaveEffect(
        color0, color1, oscillate=True, b=5, oscillation_speed_ms=1000
    )
    sine_wave.frame_speed_ms = 50
    device = neopixel.NeoPixel(
        PIXEL_PIN,
        NUM_PIXELS,
        auto_write=True,
        pixel_order=PIXEL_ORDER,
        brightness=0.5,
    )
    strip = NeoPixelStrip(device)
    player = players.LedEffectPlayer(strip, sine_wave)
    handle = player.play()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle.stop()


def play_a2b_effect():
    segment = AudioSegment.from_file("app/files/audio/poof.wav")
    segment = segment.set_sample_width(2)
    color0 = [32, 139, 25]

    device = neopixel.NeoPixel(
        PIXEL_PIN,
        NUM_PIXELS,
        auto_write=True,
        pixel_order=PIXEL_ORDER,
        brightness=0.1,
    )
    device.fill(color0)
    strip = NeoPixelStrip(device)
    a2b_effect = led_effect.AudioToBrightnessEffect(strip, segment)
    audio_player = players.AudioPlayer(segment)
    effect_player = players.LedEffectPlayer(a2b_effect)

    # Initialize the MockAudioVisualPlayer
    av_player = players.AudioVisualPlayer(effect_player, audio_player)

    handle = av_player.loop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle.stop()


# test_rpi_neopixel_sine_wave()
play_a2b_effect()
