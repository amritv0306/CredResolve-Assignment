
# CredResolve — scheme_agent

A small speech-to-text helper that uses OpenAI's transcription API (Whisper-style) to transcribe audio files and return structured results. This repository contains a minimal CLI-friendly Python script (`stt.py`) intended for offline testing and integration into larger projects.

## Features

- Transcribe local audio files using the OpenAI transcription endpoint.
- Returns a simple structured JSON-like dict containing success, text, and language (or error on failure).
- Designed to be small and easily testable. Contains a runnable example under `if __name__ == "__main__`".

## Repository layout

- `stt.py` — main speech-to-text helper. Loads `OPENAI_API_KEY` from environment (or `.env`) and calls the OpenAI audio transcription API.
- `audio/` — place audio files used for tests or manual runs (example: `audio/test_input.wav`).
- `audio_input.py`, `test.py` — auxiliary files present in the workspace.
- `requirements.txt` — project dependencies.

## Quick start

1. Install Python 3.10+ (recommended) and create a virtual environment.

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Provide your OpenAI API key. You can either create a `.env` file in the project root with:

```text
OPENAI_API_KEY=sk-...
```

or set it for the current PowerShell session like this:

```powershell
$env:OPENAI_API_KEY = 'sk-...'
```

4. Place or record an audio file into the `audio/` folder (the example uses `audio/test_input.wav`).

5. Run the transcription script:

```powershell
python stt.py
```

You should see printed progress and a final JSON-like result printed to the console.

## Configuration and notes

- SDK compatibility: This project expects an OpenAI Python SDK that exposes a transcription/audio interface. The `stt.py` code calls `client.audio.transcriptions.create(...)` with `model="gpt-4o-transcribe"` and `response_format="verbose_json"`. If your installed SDK uses a different method name (for example `openai.Audio.transcribe()`), adapt `stt.py` accordingly.
- The script currently rejects English audio by design (it returns an error when `language == 'en'`). Change that behavior in `stt.py` if you want to accept English.
- `CONFIDENCE_THRESHOLD` is defined in `stt.py` but not used — you may want to aggregate per-segment confidences from the verbose JSON response and decide whether to accept low-confidence transcriptions.

## Development & testing

- To run quick manual tests, add audio files to `audio/` and run `python stt.py`.
- For unit testing, consider refactoring `speech_to_text` to accept an injectable `client` so you can pass a mock API client in tests.

## Troubleshooting

- If you get API errors, check that `OPENAI_API_KEY` is correctly set and that the installed OpenAI SDK version matches the call pattern.
- Network errors/timeouts: wrap the API call with retries or run the script behind a reliable network.

## Contributing

If you'd like to improve this helper, suggested small tasks:

- Add robust exception handling and retries around the API call.
- Use `pathlib` and `logging` instead of `print` for better portability and testability.
- Implement confidence aggregation using `response_format="verbose_json"` segments.

## License

This project does not include a license file. Add one if you plan to share the code publicly.

---

If you'd like, I can also:

- Apply small, low-risk improvements to `stt.py` (type hints, try/except around API call, confidence handling).
- Add a minimal test harness that mocks the OpenAI client.

Tell me what you'd prefer next.
