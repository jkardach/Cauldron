import audio.audio_player as ap
import time


def play_bubble_sound():
    player = ap.PydubAudioPlayer(
        "/home/tkardach/dev/CauldronPy/app/files/audio/bubbles.wav"
    )
    handle = player.loop()
    time.sleep(10)
    handle.stop()


play_bubble_sound()
