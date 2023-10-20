from cauldron import Cauldron
import board
import neopixel
from neopixel_strip import NeoPixelStrip
import time

PIXEL_ORDER = neopixel.RGB
PIXEL_PIN = board.D12
NUM_PIXELS = 50
device = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    auto_write=True,
    pixel_order=PIXEL_ORDER,
    brightness=0.1,
)
strip = NeoPixelStrip(device)


def test_explosions():
    cauldron = Cauldron(strip)

    time.sleep(5)
    for i in range(5):
        print("Causing explosion")
        cauldron.cause_explosion()
        time.sleep(5)


test_explosions()
