import board
import led_effect
import led_strip
import neopixel
import players


class Cauldron:
    def __init__(self, strip: led_strip.LedStrip):
        self._strip = strip
