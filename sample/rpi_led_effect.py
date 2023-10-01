import led.led_effect as led
import led.led_strip as led_strip
from led.neopixel_strip import NeoPixelStrip
import matplotlib.pyplot as plt
import neopixel
import board
import numpy as np
from test_tools import TestEffect, NUM_PIXELS


PIXEL_ORDER = neopixel.RGB
PIXEL_PIN = board.D18


def test_rpi_neopixel_sine_wave():
    color0 = [3, 252, 11]
    color1 = [229, 245, 5]

    sine_wave = led.SineWaveEffect(
        color0, color1, oscillate=True, b=5, oscillation_speed_ms=250
    )
    sine_wave.frame_speed_ms = 50
    device = neopixel.NeoPixel(
        PIXEL_PIN,
        test_tools.NUM_PIXELS,
        auto_write=True,
        pixel_order=PIXEL_ORDER,
        brightness=0.5,
    )
    strip = led_strip.NeoPixelStrip(device)

    TestEffect.test_effect(strip, sine_wave)


test_rpi_neopixel_sine_wave()
