from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def summarize_text(text):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"Summarize this text clearly for a student:\n\n{text}"
    )

    return response.text