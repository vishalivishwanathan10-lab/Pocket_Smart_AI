from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_learning_recommendations(topic):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"Give a simple learning path for a student who wants to learn: {topic}"
    )

    return response.text