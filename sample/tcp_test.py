import led_effect
from led_strip import RgbArrayStrip, PixelOrder, LedStrip
from players import LedEffectPlayer, Handle
import sys
import socket


def test_bubbling_effect(strip: LedStrip):
    colors = ([142, 75, 166], [0, 255, 0])
    bubble_lengths = [7, 9, 11]
    bubble_pop_speeds = [3000, 4000, 5000]
    weights = [0.5, 0.25, 0.25]

    # bubble_effect = led_effect.BubblingEffect(
    #     strip,
    #     colors[0],
    #     colors[1],
    #     bubble_lengths,
    #     weights,
    #     bubble_pop_speeds,
    #     weights,
    #     10,
    #     0.05,
    # )
    bubble_effect = led_effect.SineWaveEffect(
        strip,
        colors[0],
        colors[1],
        oscillate=True,
        b=5,
        oscillation_speed_ms=1000,
    )
    player = LedEffectPlayer(bubble_effect)
    strip.fill(colors[0])
    return player.loop()


# echo-server.py

HOST = "192.168.0.251"  # Standard loopback interface address (localhost)
PORT = 5465  # Port to listen on (non-privileged ports are > 1023)
strip = RgbArrayStrip(50)
strip.fill((255, 0, 0))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        try:
            while True:
                brightness = int(strip.brightness * 255).to_bytes(1, "big")
                data = brightness + strip.get_pixels(PixelOrder.BGR).tobytes()
                conn.sendall(data)
        except KeyboardInterrupt:
            pass
