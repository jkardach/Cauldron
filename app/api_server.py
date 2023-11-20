from cauldron import Cauldron
from flask import Flask
from led_strip import UdpStreamStrip

app = Flask(__name__)


cauldron: Cauldron = None

NUM_PIXELS = 50
HOST = "192.168.0.4"
PORT = 5456
strip = UdpStreamStrip(NUM_PIXELS, HOST, PORT, 0.2)


@app.route("/effect/cauldron/play")
def cauldron_effect_start():
    global cauldron
    global strip
    if cauldron is None:
        cauldron = Cauldron(strip)
    cauldron.start()
    return "Success"


@app.route("/effect/cauldron/stop")
def cauldron_effect_stop():
    global cauldron
    if cauldron is None:
        return "Success"
    cauldron.stop()
    return "Success"


@app.route("/effect/cauldron/explode")
def cauldron_effect_explode():
    global cauldron
    if cauldron is None:
        return "Cauldron has not been started", 400
    cauldron.cause_explosion()
    return "Success"
