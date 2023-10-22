import rpyc
from rpyc.utils.server import ThreadedServer

import board
from cauldron import Cauldron, ICauldron
import neopixel
from neopixel_strip import NeoPixelStrip
import time


NUM_PIXELS = 50
PIXEL_ORDER = neopixel.RGB
PIXEL_PIN = board.D12
PORT_NUM = 55455


class RpycCauldronService(rpyc.Service, ICauldron):
    """Rpyc service that exposes cauldron methods to a rpyc connection."""

    def __init__(self):
        device = neopixel.NeoPixel(
            PIXEL_PIN,
            NUM_PIXELS,
            auto_write=True,
            pixel_order=PIXEL_ORDER,
            brightness=0.2,
        )
        strip = NeoPixelStrip(device)
        self._cauldron = Cauldron(strip)

    @rpyc.exposed
    def cause_explosion(self):
        self._cauldron.cause_explosion()


server = ThreadedServer(RpycCauldronService, port=PORT_NUM)
server.start()

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    pass
