import json
from audio_input import record_audio
from stt import speech_to_text
from planner import planner
from memory import ConversationMemory
from tools.eligibility_engine import check_eligibility
from tts import speak
from logger import log_info, log_error, log_warning
import re


# ================= LANGUAGE CONFIG =================

LANGUAGE_OPTIONS = {
    "hindi": "hi",
    "हिंदी": "hi",

    "telugu": "te",
    "తెలుగు": "te",

    "marathi": "mr",
    "मराठी": "mr",

    "tamil": "ta",
    "தமிழ்": "ta",

    "bengali": "bn",
    "বাংলা": "bn"
}


def select_language():
    """
    Bootstrap step:
    - Transcribe language name using English STT
    - Map to internal language code
    """

    speak(
        "Please say Hindi, Telugu, Marathi, Tamil, or Bengali to choose your language.",
        "hi"
    )

    audio_path = record_audio("audio/language_select.wav")

    # 👇 BOOTSTRAP STT: always English
    stt_result = speech_to_text(audio_path, language_hint="hi")

    if not stt_result["success"]:
        log_warning("Language selection STT failed. Defaulting to Hindi.")
        return "hi"

    spoken_text = stt_result["text"].lower()
    log_info(f"Language selection input: {spoken_text}")

    LANGUAGE_KEYWORDS = {
        "hindi": "hi",
        "हिंदी": "hi",

        "telugu": "te",
        "తెలుగు": "te",

        "marathi": "mr",
        "मराठी": "mr",

        "tamil": "ta",
        "தமிழ்": "ta",

        "bengali": "bn",
        "বাংলা": "bn"
    }

    for keyword, lang_code in LANGUAGE_KEYWORDS.items():
        if keyword in spoken_text:
            return lang_code

# ================= Extract Numbers =================
def extract_numbers(text):
    """
    Extracts integers from noisy speech text.
    Handles: 22, 22 साल, ₹50000, 50,000
    """
    matches = re.findall(r"\d+", text)
    return [int(m) for m in matches]


# ================= AGENT LOOP =================

def agent_loop():
    log_info("Agent started")
    print("\n" + "="*30)
    print("🚀 VOICE-BASED AGENT")
    print("="*30)

    # 1. Language Selection
    language = select_language()
    log_info(f"User selected language: {language}")
    print(f"🌐 Language set to: {language}")
    
    # 2. Initial Greeting & Question
    greet_text = {
        "te": "నమస్కారం, దయచేసి మీ ప్రశ్న చెప్పండి.",
        "hi": "नमस्ते, कृपया अपना प्रश्न बताएं।",
        "mr": "नमस्कार, कृपया तुमचा प्रश्न सांगा.",
        "ta": "வணக்கம், தயவுசெய்து உங்கள் கேள்வியை கூறுங்கள்.",
        "bn": "নমস্কার, অনুগ্রহ করে আপনার প্রশ্ন বলুন।"
    }
    speak(greet_text.get(language, greet_text["hi"]), language)

    # 3. Capture Initial Request
    audio_path = record_audio("audio/init.wav")
    stt_result = speech_to_text(audio_path, language_hint=language)
    
    memory = ConversationMemory(language)
    if stt_result["success"]:
        memory.add_user_utterance(stt_result["text"])

    # 3. Targeted Sequential Collection
    # We define the order: Age -> Income -> State
    required_fields = ["age", "income", "state"]
    
    for field in required_fields:
        attempts = 0
        while attempts < 3:
            # Check if we already have it from the initial query
            current_profile = memory.get_memory_snapshot()["profile"]
            if current_profile.get(field) is not None:
                print(f"✅ Already have {field}: {current_profile[field]}")
                break
            
            # System asks specifically for the missing field
            prompts = {
                "age": ("आपकी उम्र क्या है?", "మీ వయస్సు ఎంత?"),
                "income": ("आपकी वार्षिक आय क्या है?", "మీ వార్షిక ఆదాయం ఎంత?"),
                "state": ("आप किस राज्य में रहते हैं?", "మీరు ఏ రాష్ట్రంలో నివసిస్తున్నారు?")
            }
            speak(prompts[field][0] if language == "hi" else prompts[field][1], language)
            
            audio_path = record_audio(f"audio/{field}_retry_{attempts}.wav")
            stt_result = speech_to_text(audio_path, language_hint=language)
            
            if stt_result["success"]:
                val = stt_result["text"].lower()
                print(f"🗨️ User said for {field}: {val}")
                
                if field in ["age", "income"]:
                    nums = extract_numbers(val)
                    if nums:
                        # Logic Fix: If asking for income, take the largest number or the second number
                        # if the user said "My age is 7 and income is 20000"
                        extracted_val = nums[-1] if len(nums) > 1 else nums[0]
                        memory.update_profile(field, extracted_val)
                        print(f"DEBUG: Saved {field} -> {extracted_val}")
                        break
                
                if field == "state":
                    # Improved detection including Native Script
                    if any(s in val for s in ["telangana", "తెలంగాణ", "तेलंगाना"]):
                        memory.update_profile("state", "telangana")
                        break
                    elif any(s in val for s in ["maharashtra", "महाराष्ट्र", "మహారాష్ట్ర"]):
                        memory.update_profile("state", "maharashtra")
                        break
            
            attempts += 1
            print(f"⚠️ Failed to catch {field}, attempt {attempts}/3")

    # 4. Final Tool Execution
    final_profile = memory.get_memory_snapshot()["profile"]
    print(f"\n📊 FINAL PROFILE FOR TOOL: {final_profile}")
    
    result = check_eligibility(final_profile)
    log_info(f"Tool Result: {result}")

    # 5. Result Output
    if result.get("eligible"):
        schemes = ", ".join(result["eligible"])
        response = f"आप {schemes} के लिए पात्र हैं।" if language == "hi" else f"మీరు {schemes}కు అర్హులు."
    else:
        error_msg = result.get("error", "कोई योजना नहीं मिली")
        response = f"क्षमा करें: {error_msg}" if language == "hi" else f"క్షమించండి: {error_msg}"

    speak(response, language)
    speak("धन्यवाद।" if language == "hi" else "ధన్యవాదాలు.", language)

if __name__ == "__main__":
    agent_loop()