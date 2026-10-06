from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def explain_topic(topic):

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
Explain this topic clearly for a student.

Topic: {topic}

Give:
1. Simple definition
2. Key concepts
3. Easy example
4. Practical uses
"""
        )

        return response.text

    except Exception as error:
        print("Gemini Error:", error)
        raise error