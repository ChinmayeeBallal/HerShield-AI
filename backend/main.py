from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
from fastapi import UploadFile, File
import hashlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    image_bytes = await file.read()

    fingerprint = hashlib.sha256(image_bytes).hexdigest()

    hash_int = int(fingerprint[:8], 16)
    probability = hash_int % 100

    if probability > 75:
        level = "Critical"
    elif probability > 50:
        level = "Warning"
    else:
        level = "Safe"

    return {
        "probability": probability,
        "level": level,
        "fingerprint": fingerprint
    }