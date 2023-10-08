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


def test_bubble_effect():
    color0 = [32, 139, 25]
    color1 = [43, 199, 32]

    bubble_effect = led_effect.BubbleEffect(
        int(NUM_PIXELS / 2), color0, color1, bubble_length=9
    )
    mock_strip = led_strip.MockStrip(NUM_PIXELS)
    player = MockEffectPlayer(mock_strip, bubble_effect)
    mock_strip.fill(color0)
    handle = player.play()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle.stop()


# test_mock_sine_wave()
test_bubble_effect()
