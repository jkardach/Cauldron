import board
import led_effect
from neopixel_strip import NeoPixelStrip
import neopixel
from players import LedEffectPlayer
import time


PIXEL_ORDER = neopixel.RGB
PIXEL_PIN = board.D18
NUM_PIXELS = 50


def test_rpi_neopixel_sine_wave():
    color0 = [3, 252, 11]
    color1 = [229, 245, 5]

    sine_wave = led_effect.SineWaveEffect(
        color0, color1, oscillate=True, b=5, oscillation_speed_ms=250
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
    player = LedEffectPlayer(strip, sine_wave)
    handle = player.play()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle.stop()


test_rpi_neopixel_sine_wave()
