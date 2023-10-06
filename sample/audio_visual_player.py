import led_effect
import led_strip
import players
from pydub import AudioSegment
import time


NUM_PIXELS = 50


def play_bubble_effect():
    # Initialize the AudioPlayer
    segment = AudioSegment.from_file("app/files/audio/bubbles.wav")
    segment.frame_rate = int(segment.frame_rate / 2)
    audio_player = players.AudioPlayer(segment)

    color0 = [3, 252, 11]
    color1 = [229, 245, 5]

    # Initialize the MockEffectPlayer
    sine_wave = led_effect.SineWaveEffect(
        color0, color1, oscillate=True, b=5, oscillation_speed_ms=1000
    )
    mock_strip = led_strip.MockStrip(NUM_PIXELS)
    effect_player = players.MockEffectPlayer(mock_strip, sine_wave)

    # Initialize the MockAudioVisualPlayer
    av_player = players.MockAudioVisualPlayer(effect_player, audio_player)

    # Loop the player until a keyboard interrupt is received
    handle = av_player.loop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle.stop()


play_bubble_effect()
