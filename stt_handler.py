import torch
from transformers import pipeline
from ai4bharat.IndicLID import IndicLID # Ensure you have followed AI4Bharat installation for IndicLID

class AI4BharatSTT:
    def __init__(self, asr_model_path="ai4bharat/indicwhisper-hindi"):
        # 1. Initialize ASR (Speech-to-Text) Pipeline
        # You can swap model_path for other languages like 'indicwhisper-marathi'
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.asr_pipeline = pipeline(
            "automatic-speech-recognition", 
            model=asr_model_path, 
            device=self.device
        )
        
        # 2. Initialize Language Identifier (LID)
        # Note: Follow local installation from AI4Bharat GitHub for the model files
        self.lid_model = IndicLID(input_threshold=0.5, roman_lid_threshold=0.6)

    def process_audio(self, audio_path):
        """Transcribes audio and validates language."""
        try:
            # Step A: Transcribe audio to text
            transcription = self.asr_pipeline(audio_path)
            text = transcription.get("text", "").strip()

            # Step B: Failure Handling - Check for empty transcription
            if not text:
                return {
                    "success": False,
                    "error": "Empty transcription"
                }

            # Step C: Detect Language using IndicLID
            # IndicLID identifies if the text is in native script, romanized, or English
            predictions = self.lid_model.predict(text)
            # Example prediction output: {'lang': 'hi', 'score': 0.9}
            language = predictions.get("lang", "unknown")

            # Step D: Filter English
            if language == "en":
                return {
                    "success": False,
                    "error": "English detected. Please speak in a native Indian language."
                }

            # Step E: Return Successful Result
            return {
                "success": True,
                "text": text,
                "language": language
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

if __name__ == "__main__":
    # Example usage:
    stt = AI4BharatSTT()
    result = stt.process_audio("user_request.wav")
    print(result)