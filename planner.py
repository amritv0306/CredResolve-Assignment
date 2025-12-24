import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def extract_json(text):
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end+1])
    except json.JSONDecodeError:
        return None

def planner(user_text, memory, language):
    """
    user_text: str (native language)
    memory: dict (conversation memory so far)
    language: detected language code
    """

    system_prompt = f"""
        You are an AI service agent helping users apply for government welfare schemes.

        STRICT RULES (DO NOT VIOLATE):
        - Respond ONLY with a valid JSON object
        - Do NOT add explanations, comments, or markdown
        - Do NOT wrap JSON in backticks
        - Output must start with {{ and end with }}

        Your task:
        1. Identify user intent
        2. Identify missing eligibility fields
        3. Decide next action

        Eligibility fields:
        - age
        - income
        - state

        Allowed next_action values:
        - ask_user
        - call_tool
        - end_conversation

        IMPORTANT RULE:
        - If missing_fields is empty, you MUST choose next_action = call_tool
        - NEVER end the conversation before calling the tool

        Language rule:
        - Use the user's native language for questions
        """

    user_prompt = f"""
        User language: {language}

        Conversation memory:
        {json.dumps(memory, ensure_ascii=False)}

        User said:
        {user_text}

        Return JSON with keys:
        intent, missing_fields, next_action, question (if next_action is ask_user)
        """

    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=system_prompt + "\n" + user_prompt
    )

    """try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=system_prompt + "\n" + user_prompt
        )
    except Exception as e:
        return {
            "intent": "error",
            "next_action": "ask_user",
            "question": "कृपया थोड़ी देर बाद फिर से प्रयास करें।"
        }"""

    raw_text = response.text.strip()
    parsed = extract_json(raw_text)

    if parsed:
        return parsed

    return {
        "intent": "unknown",
        "next_action": "ask_user",
        "question": "క్షమించండి, మళ్లీ చెప్పగలరా?"
    }


# 🧪 TEST
if __name__ == "__main__":
    test_memory = {}
    test_text = "నాకు ఏ ప్రభుత్వ పథకాలకు అర్హత ఉందో తెలుసుకోవాలి"
    lang = "te"

    output = planner(test_text, test_memory, lang)
    print(json.dumps(output, indent=2, ensure_ascii=False))
