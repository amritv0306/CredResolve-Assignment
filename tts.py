from gtts import gTTS
import pygame
import os
import time

LANGUAGE_MAP = {
    "hi": "hi",
    "te": "te",
    "ta": "ta",
    "mr": "mr",
    "bn": "bn"
}

def speak(text, language="hi"):
    lang_code = LANGUAGE_MAP.get(language, "hi")

    os.makedirs("audio", exist_ok=True)
    filename = f"audio/tts_{int(time.time())}.mp3"

    tts = gTTS(text=text, lang=lang_code)
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    try:
        os.remove(filename)
    except:
        pass

    
if __name__ == "__main__":
    speak("नमस्ते! यह एक परीक्षण है।", language="hi")
    speak("హలో! ఇది ఒక పరీక్ష.", language="te")
    speak("வணக்கம்! இது ஒரு சோதனை.", language="ta")
    speak("नमस्कार! ही एक चाचणी आहे.", language="mr")
    speak("হ্যালো! এটি একটি পরীক্ষা।", language="bn")