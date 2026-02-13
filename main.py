from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI, RateLimitError
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")  # IMPORTANT
)

class UserMessage(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "SpeakFree AI running"}

@app.post("/chat")
def chat(user: UserMessage):

    if not user.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    system_prompt = (
        "You are a friendly AI confidence coach and English tutor.\n"
        "Detect emotion, correct English gently, encourage the user.\n"
        "Keep responses short and supportive."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user.message}
            ],
            max_tokens=150,
            temperature=0.7
        )

        return {
            "reply": response.choices[0].message.content
        }

    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="API quota exceeded."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )
