import led_effect
import led_strip
from players import MockEffectPlayer
import time


NUM_PIXELS = 50


def test_mock_sine_wave():
    color0 = [3, 252, 11]
    color1 = [229, 245, 5]

    sine_wave = led_effect.SineWaveEffect(
        color0, color1, oscillate=True, b=5, oscillation_speed_ms=1000
    )
    mock_strip = led_strip.MockStrip(NUM_PIXELS)
    player = MockEffectPlayer(mock_strip, sine_wave)
    handle = player.play()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle.stop()


test_mock_sine_wave()
