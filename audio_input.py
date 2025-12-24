import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time
import os

SAMPLE_RATE = 16000  # standard for STT
CHANNELS = 1
RECORD_SECONDS = 8   # we’ll adjust later

def record_audio(filename="user_input.wav"):
    print("\n🎙️ Recording will start in 2 seconds...")
    time.sleep(2)
    print("🔴 Recording... Speak now")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=np.int16
    )

    sd.wait()
    write(filename, SAMPLE_RATE, audio)

    print(f"✅ Recording saved as: {filename}")
    return filename


if __name__ == "__main__":
    os.makedirs("audio", exist_ok=True)
    filepath = os.path.join("audio", "test_input.wav")
    record_audio(filepath)