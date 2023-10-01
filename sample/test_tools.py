import led.led_effect as led_effect
import led.led_strip as led_strip
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import time


NUM_PIXELS = 50


class TestEffect:
    @staticmethod
    def test_effect(strip: led_strip.LedStrip, effect: led_effect.LedEffect):
        if isinstance(strip, led_strip.MockStrip):
            return MockEffect.test_effect(strip, effect)

        try:
            print("Press Ctrl-C to exit")
            while True:
                effect.apply_effect(strip)
                time.sleep(effect.frame_speed_ms / 1000.0)
        except KeyboardInterrupt:
            pass


class MockEffect:
    @staticmethod
    def test_effect(strip: led_strip.LedStrip, effect: led_effect.LedEffect):
        x = np.arange(0, strip.num_pixels(), 1)
        y = [3] * strip.num_pixels()
        fig, ax = plt.subplots()
        ax.set(xlim=[0, NUM_PIXELS], ylim=[0, 6])

        # Create scatter plot to simulate LEDs
        scat = plt.scatter(x, y, s=50)

        # Create set_pixels callback to change the LED scatter plot dot colors
        def set_pixels(pixels: np.array):
            scat.set_color(pixels / 255.0)

        # Set the show callback to update the pixel colors. This will call
        # set_pixels when LedStrip.show is called.
        strip.set_show_callback(set_pixels)

        # Create the pyplot animation update method. This will update the
        # LedStrip pixels
        def update(frame):
            effect.apply_effect(strip)
            return scat

        ani = animation.FuncAnimation(
            fig=fig, func=update, frames=40, interval=effect.frame_speed_ms
        )
        try:
            print("Press Ctrl-C to exit")
            plt.show()
        except KeyboardInterrupt:
            pass
