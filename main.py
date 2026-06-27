from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import cv2
import numpy as np

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

    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:
        return {
            "probability": 0,
            "level": "Error",
            "fingerprint": fingerprint
        }

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size

    probability = int(
        min(
            100,
            (edge_density * 1000) + (1000 / (laplacian_var + 1))
        )
    )

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