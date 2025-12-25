from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="SpeakFree AI Backend")

# --------------------
# Health Check
# --------------------
@app.get("/")
def health():
    return {"status": "ok", "service": "SpeakFree AI Backend"}

# --------------------
# AI Request Model
# --------------------
class AIRequest(BaseModel):
    prompt: str

# --------------------
# AI Endpoint (Mock / Real)
# --------------------
@app.post("/ai/chat")
def ai_chat(data: AIRequest):
    # TEMP: replace this with your real AI logic later
    return {
        "response": f"AI received your message: {data.prompt}"
    }
