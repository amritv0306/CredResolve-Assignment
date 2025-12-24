import os
from dotenv import load_dotenv
from google.cloud import speech_v1p1beta1 as speech
from audio_input import record_audio
from tts import speak

load_dotenv()

# Google STT client
client = speech.SpeechClient()

# ================= LANGUAGE MAP =================

LANGUAGE_MAP = {
    "hi": "hi-IN",
    "te": "te-IN",
    "ta": "ta-IN",
    "mr": "mr-IN",
    "bn": "bn-IN"
}

LANGUAGE_CONFIRM_TEXT = {
    "hi": "आपने हिंदी चुनी है। क्या हम हिंदी में आगे बढ़ें? हाँ या नहीं कहें।",
    "te": "మీరు తెలుగు ఎంచుకున్నారు. మనం తెలుగులో కొనసాగాలా? అవును లేదా కాదు చెప్పండి.",
    "ta": "நீங்கள் தமிழை தேர்ந்தெடுத்துள்ளீர்கள். தமிழில் தொடரலாமா? ஆம் அல்லது இல்லை சொல்லுங்கள்.",
    "mr": "तुम्ही मराठी निवडली आहे. आपण मराठीत पुढे जाऊ का? हो किंवा नाही सांगा.",
    "bn": "আপনি বাংলা নির্বাচন করেছেন। আমরা কি বাংলায় এগিয়ে যাব? হ্যাঁ বা না বলুন।"
}

YES_WORDS = {
    "hi": ["हाँ", "haan", "ha"],
    "te": ["అవును"],
    "ta": ["ஆம்"],
    "mr": ["हो"],
    "bn": ["হ্যাঁ"]
}

NO_WORDS = {
    "hi": ["नहीं", "nahin", "nahi"],
    "te": ["కాదు"],
    "ta": ["இல்லை"],
    "mr": ["नको", "नाही"],
    "bn": ["না"]
}

# ================= LANGUAGE CONFIRMATION =================

def confirm_language(language_code):
    """
    Asks user to confirm selected language via voice.
    Returns True if confirmed, False otherwise.
    """

    speak(LANGUAGE_CONFIRM_TEXT[language_code], language_code)

    audio_path = record_audio("audio/language_confirm.wav")
    result = speech_to_text(audio_path, language_code)

    if not result["success"]:
        return False

    reply = result["text"].lower()

    if any(word in reply for word in YES_WORDS[language_code]):
        return True

    if any(word in reply for word in NO_WORDS[language_code]):
        return False

    return False


# ================= SPEECH TO TEXT =================

def speech_to_text(audio_path, language_hint):
    """
    Converts speech to text using STRICT language locking.
    """

    if not os.path.exists(audio_path):
        return {
            "success": False,
            "error": "Audio file not found"
        }

    if language_hint not in LANGUAGE_MAP:
        return {
            "success": False,
            "error": "Unsupported language"
        }

    with open(audio_path, "rb") as audio_file:
        audio_content = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=LANGUAGE_MAP[language_hint],
        enable_automatic_punctuation=True
    )

    try:
        response = client.recognize(config=config, audio=audio)
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    if not response.results:
        return {
            "success": False,
            "error": "No speech detected"
        }

    alternative = response.results[0].alternatives[0]

    return {
        "success": True,
        "text": alternative.transcript.strip(),
        "language": language_hint,
        "confidence": alternative.confidence
    }


# ================= LOCAL TEST =================
if __name__ == "__main__":
    print("STT module ready with strict language locking and confirmation.")
    # print(speech_to_text("audio/test_input.wav", language_hint="hi"))
