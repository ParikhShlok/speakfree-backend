from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from openai import OpenAI
from supabase import create_client
from upload import router as upload_router

import os
from database import engine
from models import Base

#Base.metadata.create_all(bind=engine)

app = FastAPI()


# ---------------- Routes ----------------
@app.get("/")
def home():
    return {"status": "SpeakFree AI running"}

# 🧠 SpeakFree AI
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

    return {"reply": response.choices[0].message.content}



