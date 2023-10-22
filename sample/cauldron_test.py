import board
from cauldron import Cauldron
import neopixel
from neopixel_strip import NeoPixelStrip
import threading
import time

PIXEL_ORDER = neopixel.RGB
PIXEL_PIN = board.D12
NUM_PIXELS = 50
device = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    auto_write=True,
    pixel_order=PIXEL_ORDER,
    brightness=0.2,
)
strip = NeoPixelStrip(device)


def wait_for_explosion():
    cauldron = Cauldron(strip)
    try:
        while True:
            user = input("Press Enter")
            if user == "":
                print("Causing explosion")
                cauldron.cause_explosion()
            elif user == "esc":
                return
    except KeyboardInterrupt:
        cauldron = None


def test_explosions():
    t = threading.Thread(target=wait_for_explosion)
    t.start()
    t.join()


def test_default():
    cauldron = Cauldron(strip)

    time.sleep(60)


test_explosions()
# test_default()
