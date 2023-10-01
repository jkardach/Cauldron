import led.led_effect as led
import led.led_strip as led_strip
import matplotlib.pyplot as plt
import numpy as np
from test_tools import TestEffect, NUM_PIXELS


def test_mock_sine_wave():
    color0 = [3, 252, 11]
    color1 = [229, 245, 5]

    sine_wave = led.SineWaveEffect(
        color0, color1, oscillate=True, b=5, oscillation_speed_ms=1000
    )
    mock_strip = led_strip.MockStrip(NUM_PIXELS)
    TestEffect.test_effect(mock_strip, sine_wave)


test_mock_sine_wave()
