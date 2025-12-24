# 🎙️ Voice-Based Native Language Welfare Scheme Assistant

A **voice-first, agentic AI system** that helps users identify **eligible government welfare schemes** using **native Indian languages**.  
The system performs **end-to-end speech interaction**, autonomous reasoning, tool usage, conversation memory, and failure handling.

This project is built to satisfy **all mandatory requirements** of the assignment:
- Voice-first interaction
- Native (non-English) language pipeline
- True agentic workflow
- Tool usage
- Memory across turns
- Failure recovery

---

## 🚀 Key Features

- 🎧 **Voice-first interaction** (Speech → Reasoning → Speech)
- 🌐 **Native language support**
  - Hindi
  - Telugu
  - Marathi
  - Tamil
  - Bengali
- 🧠 **Agentic workflow** (Planner → Memory → Tool → Response)
- 🛠️ **Tool-based eligibility computation**
- 🧾 **Conversation memory across turns**
- 🧯 **Failure handling for missing or unclear input**
- 🔒 **Language locking** (no language drift once selected)
- 📊 **Data-driven eligibility using `schemes.json`**

---

## 🏗️ High-Level Architecture


User Voice <br>
   ↓<br>
Speech-to-Text (Google STT)<br>
   ↓<br>
Agent Planner (Gemini LLM)<br>
   ↓<br>
Conversation Memory<br>
   ↓<br>
Eligibility Engine (JSON-driven)<br>
   ↓<br>
Text-to-Speech (gTTS)<br>
   ↓<br>
User Voice Output<br>


---

## 📁 Project Structure

```
scheme_agent/
│
├── agent_loop.py              # Main agent orchestration loop
├── planner.py                 # LLM-based planner (Gemini)
├── memory.py                  # Conversation memory & profile state
├── audio_input.py             # Voice recording utility
├── stt.py                     # Speech-to-text (Google Cloud STT)
├── tts.py                     # Text-to-speech (gTTS)
├── logger.py                  # Logging utility
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (NOT committed)
├── .gitignore
│
├── tools/
│   ├── eligibility_engine.py  # Scheme eligibility logic
│   ├── scheme_retriever.py    # Scheme retrieval helper
│   └── schemes.json           # Government schemes dataset
│
├── credentials/
│   └── google_stt_key.json    # Google STT service account key
│
├── audio/                     # Temporary audio files
├── logs/                      # Runtime logs
└── venv/                      # Python virtual environment
```
---

## 🧠 Agent Workflow (How It Works)

- Language Selection
    - User selects preferred language via voice
    - System locks this language for the entire session

- Intent Understanding

    - Planner determines user intent (e.g., scheme eligibility)

- Information Collection

    - Agent sequentially collects:

        - Age

        - Income

        - State

    - Uses memory to track missing fields

- Eligibility Evaluation

    - eligibility_engine.py reads schemes.json

    - Filters schemes based on user profile

- Voice Response

    - Eligible schemes are spoken back in the selected language

- Graceful Termination

    - Conversation ends cleanly after response

--- 
## 🛠️ Tools Used

- Speech-to-Text (STT)

    - Google Cloud Speech-to-Text

    - Strict language locking per session

    - Requires service account credentials

- Planner (LLM)

    - Google Gemini API

    - Produces structured JSON decisions

    - Enforces agentic control (no free-text responses)

- Eligibility Engine

    - Fully data-driven

    - Uses schemes.json as the single source of truth

    - No hardcoded scheme logic

---

## 📦 Setup Instructions (Step-by-Step)

### ✅ 1. Clone the Repository

```
git clone <your-repo-url>
cd scheme_agent
```

### ✅ 2. Create Virtual Environment

```
python -m venv venv
```
Activate it:

```
venv\Scripts\activate
```

### ✅ 3. Install Dependencies

```
pip install -r requirements.txt
```

### ✅ 4. Google Cloud STT Setup

- Create a Google Cloud Project

- Enable Speech-to-Text API

- Create a Service Account
 
- Download the key as JSON
 
- Place it inside:
```
credentials/google_stt_key.json
```

- Set environment variable:
```
setx GOOGLE_APPLICATION_CREDENTIALS "credentials/google_stt_key.json"
```

### ✅ 5. Gemini API Setup

Create a .env file in the root directory:
```
.env
```

Add:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
⚠️ .env is ignored via .gitignore for security.


### ✅ 6. Verify Audio Setup

- Make sure your system has:

    - Working microphone

    - Speaker / headphones

Test recording:
```
python audio_input.py
```

### ✅ 7. Run the Agent
```
python agent_loop.py
```

---

## 🧪 Example Interaction
User (Voice):

**“I want to know which government schemes I am eligible for.”**

Agent (Voice):

- Asks age

- Asks income

- Asks state

- Returns eligible schemes

All interactions happen entirely in the chosen native language.

---

## 📊 schemes.json (Data Format)

Each scheme follows this structure:
```
{
  "name": "Telangana State Support Scheme",
  "state": "telangana",
  "max_age": 35,
  "max_income": 300000
}
```
You can add or modify schemes without changing any code.

--- 
## 🧯 Failure Handling

- Re-prompts user if speech is unclear

- Handles missing inputs gracefully

- Prevents infinite loops

- Stops cleanly on tool or API failure

---

## 🔐 Security & Best Practices

- API keys stored in `.env`

- Credentials excluded via `.gitignore`

- Temporary audio files auto-cleaned

- Logs stored locally for debugging

---

## 📊 Evaluation Metrics

- **Transcripts:** Found in the `logs/` folder after every run.

- **Memory:** Local state is automatically deleted at the end of each `agent_loop()` call

- **Debugging:** View the real-time terminal output to see extracted profile data (Age, Income, State) after each user turn.


---

## 🏁 Conclusion
This project demonstrates:

- True agentic AI behavior

- Robust voice-first system design

- Practical tool-driven reasoning

- Production-grade error handling


