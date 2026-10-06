from pathlib import Path
import os 

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from google import genai
from dotenv import load_dotenv

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie AI",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# -----------------------------
# Request Models
# -----------------------------

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="inbox.html",
        context={"request": request}
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie AI"
    }


# -----------------------------
# Q&A
# -----------------------------

@app.post("/ask")
async def ask(question: str = Form(...)):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=question
        )

        return {
            "answer": response.text,
            "source": "Gemini AI"
        }

    except Exception as error:
        print("Gemini Error:", error)

        raise HTTPException(
            status_code=500,
            detail=f"Gemini API Error: {str(error)}"
        )
# Explain
# -----------------------------

@app.post("/explain")
async def explain(request: TextRequest):

    try:

        answer = explain_topic(
            request.text
        )

        return {
            "result": answer
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -----------------------------
# Quiz
# -----------------------------

@app.post("/quiz")
async def quiz(request: TextRequest):

    try:

        result = generate_quiz(
            request.text
        )

        return {
            "result": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -----------------------------
# Summary
# -----------------------------

@app.post("/summarize")
async def summarize(request: TextRequest):

    try:

        result = summarize_text(
            request.text
        )

        return {
            "result": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -----------------------------
# Learning Path
# -----------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    request: TextRequest
):

    try:

        result = get_learning_recommendations(
            request.text
        )

        return {
            "result": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )