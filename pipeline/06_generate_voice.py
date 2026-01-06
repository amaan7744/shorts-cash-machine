import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_voice(script):
    model = genai.GenerativeModel("models/gemini-2.0-flash-tts")

    response = model.generate_content(
        script,
        generation_config={
            "audio": {"voice": "neutral"}
        }
    )

    output = "data/voice.wav"
    with open(output, "wb") as f:
        f.write(response.audio)

    return output
