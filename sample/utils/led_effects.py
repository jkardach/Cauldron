from led_strip import LedStrip
import led_effect


def create_bubbling_effect(
    strip: LedStrip,
    base_color: list,
    bubble_color: list,
    bubble_lengths: list = [7, 9, 11],
    bubble_pop_speeds: list = [3000, 4000, 5000],
    weights: list = [0.5, 0.25, 0.25],
) -> led_effect.BubblingEffect:
    bubble_lengths = [7, 9, 11]
    bubble_pop_speeds = [3000, 4000, 5000]
    weights = [0.5, 0.25, 0.25]

    return led_effect.BubblingEffect(
        strip,
        base_color,
        bubble_color,
        bubble_lengths,
        weights,
        bubble_pop_speeds,
        weights,
        10,
        0.05,
    )
