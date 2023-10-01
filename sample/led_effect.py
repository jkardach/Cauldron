import board
import led.led_effect as led
import led.led_strip as led_strip
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import neopixel
import numpy as np
import time

NUM_PIXELS = 50
PIXEL_ORDER = neopixel.RGB
PIXEL_PIN = board.D18

class TestEffect():
    x = np.arange(0, NUM_PIXELS, 1)
    y = [3] * NUM_PIXELS

    @staticmethod
    def callback(pixels: np.array):
        plt.scatter(TestEffect.x, TestEffect.y, c = pixels / 255.0, s=50)

    @staticmethod
    def test_effect(strip: led_strip.LedStrip, effect: led.LedEffect):
        if isinstance(strip, led_strip.MockStrip):
            strip.set_show_callback(TestEffect.callback)
        plt.ion()
        for i in range(100):
            effect.apply_effect(strip)
            plt.pause(effect.frame_speed_ms / 1000)

        plt.show()


def test_mock_sine_wave():
    color0 = [3, 252, 11]
    color1 = [229, 245, 5]
    
    sine_wave = led.SineWaveEffect(color0, color1, oscillate = True, b = 5, oscillation_speed_ms = 150) 
    mock_strip = led_strip.MockStrip(NUM_PIXELS)

    TestEffect.test_effect(mock_strip, sine_wave)

def test_bubble_effect():
    base_color = [0, 0 ,0]
    bubble_color = [50, 255, 50]
    
    sine_wave = led.BubbleEffect(base_color, bubble_color, bubble_index = int(NUM_PIXELS/3), num_pixels=NUM_PIXELS, bubble_pop_speed_ms=250)
    mock_strip = led_strip.MockStrip(NUM_PIXELS)

    TestEffect.test_effect(mock_strip, sine_wave)

def test_rpi_neopixel_sine_wave():
    color0 = [3, 252, 11]
    color1 = [229, 245, 5]
    
    sine_wave = led.SineWaveEffect(color0, color1, oscillate = True, b = 5, oscillation_speed_ms = 50)
    device = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, auto_write=True, pixel_order=PIXEL_ORDER, brightness=0.5)
    mock_strip = led_strip.NeoPixelStrip(device)

    TestEffect.test_effect(mock_strip, sine_wave)


# test_bubble_effect()
# test_mock_sine_wave()
# test_rpi_neopixel_sine_wave()
device = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, auto_write=True, pixel_order=PIXEL_ORDER, brightness=0.5)
while True:
    device.fill([255 , 0, 0])
    time.sleep(5)
    device.fill([0 , 0, 255])
    time.sleep(5)
    device.fill([0 , 255, 0])
    time.sleep(5)
    device.fill([255 , 0, 255])
    time.sleep(5)
    device.fill([0 , 255, 255])
    time.sleep(5)
    device.fill([255 , 255, 0])
    time.sleep(5)

