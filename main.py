from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class UserMessage(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "SpeakFree AI running"}

@app.post("/chat")
def chat(user: UserMessage):

    system_prompt = (
        "You are a friendly AI confidence coach and English tutor.\n"
        "Detect emotion, correct English gently, encourage the user.\n"
        "Keep responses short and supportive."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user.message}
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }
