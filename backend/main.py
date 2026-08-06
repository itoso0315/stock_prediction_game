

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stock Trainer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_QUESTIONS_PATH = BASE_DIR / "sample_questions.json"


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/questions")
def get_questions():
    with SAMPLE_QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)