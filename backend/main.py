
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os, requests
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

GROQ_KEY = os.getenv("GROQ_API_KEY")

class PlanIn(BaseModel):
    subjects: list
    exam_date: str
    hours_per_day: int

@app.post("/generate_plan")
def generate_plan(p: PlanIn):
    if not GROQ_KEY:
        return {"error": "GROQ_API_KEY not found in .env"}

    prompt = f"Create a short study plan for subjects {p.subjects} before {p.exam_date} studying {p.hours_per_day} hours a day."

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_KEY}"},
        json={
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    j = r.json()
    if "choices" not in j:
        return {"error": j}

    return {"plan": j["choices"][0]["message"]["content"]}

# serve frontend
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
