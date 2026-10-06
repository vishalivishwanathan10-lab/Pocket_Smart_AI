from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def answer_question(question):
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=question
    )

    return response.text