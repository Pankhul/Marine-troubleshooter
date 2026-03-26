from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os

# Configure API
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="Marine Troubleshooter")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static HTML
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

class QueryInput(BaseModel):
    symptom: str

@app.post("/troubleshoot")
async def troubleshoot(input: QueryInput):
    """Ask the model to generate a troubleshooting guide."""
    prompt = f"""
    You are a marine engineer assistant. The user reports:
    "{input.symptom}"

    Give 3–5 possible causes and step‑by‑step checks to diagnose and fix it.
    Keep answers concise and technical.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350,
            temperature=0.3,
        )
        answer = response.choices[0].message["content"].strip()
    except Exception as e:
        answer = f"Error generating response: {e}"

    return {"symptom": input.symptom, "advice": answer}
