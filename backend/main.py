from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analyze")
def analyze():
    probability = random.randint(20, 95)

    if probability > 75:
        level = "Critical"
    elif probability > 50:
        level = "High"
    else:
        level = "Medium"

    return {
        "probability": probability,
        "riskLevel": level,
        "faceStatus": "1 Face Detected",
        "fingerprint": f"HS-DEMO-{random.randint(100,999)}"
    }