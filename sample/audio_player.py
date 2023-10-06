from players import AudioPlayer
from pydub import AudioSegment
import time


def play_bubble_sound():
    segment = AudioSegment.from_file("app/files/audio/bubbles.wav")
    segment.frame_rate = int(segment.frame_rate / 2)
    player = AudioPlayer(segment)
    handle = player.loop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle.stop()


play_bubble_sound()
