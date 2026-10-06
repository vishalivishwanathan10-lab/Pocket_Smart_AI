from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_quiz(topic):

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
Create 5 multiple choice questions for a student about:
{topic}

Give 4 options for each question and show the correct answer.
"""
        )

        return response.text

    except Exception as error:

        print("Gemini unavailable:", error)

        return f"""
EduGenie Demo Quiz – {topic}

1. What is {topic}?
A) A programming concept
B) A computer virus
C) A hardware device
D) An operating system

Answer: A

2. Why is {topic} useful?
A) For learning and problem solving
B) Only for gaming
C) Only for music
D) None

Answer: A

3. Which is important when learning {topic}?
A) Practice
B) Avoiding practice
C) Ignoring examples
D) None

Answer: A

Note: This is EduGenie Demo Mode because Gemini API quota is currently unavailable.
"""