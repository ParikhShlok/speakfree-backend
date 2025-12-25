from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from openai import OpenAI
from supabase import create_client
from upload import router as upload_router

import os

app = FastAPI()
app.include_router(upload_router)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- OpenAI ----------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------- Supabase ----------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials not found")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- Schemas ----------------
class UserMessage(BaseModel):
    message: str

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

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

# 🔐 Signup (Supabase)
@app.post("/signup")
def signup(data: SignupRequest):

    # Check if email already exists
    existing = supabase.table("users") \
        .select("id") \
        .eq("email", data.email) \
        .execute()

    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Insert user
    supabase.table("users").insert({
        "name": data.name,
        "email": data.email,
        "password": data.password   # hashing later (V2)
    }).execute()

    return {"message": "User registered successfully"}

