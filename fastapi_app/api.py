from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import os
import base64
import requests

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À sécuriser en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = ".."  # ⚠️ Remplace par ta clé

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def test():
    return {"message": "API FastAPI + Gemini Vision prête ✅"}

@app.post("/generate_image_ai")
async def generate_image_ai(
    main_image: UploadFile = File(...),
    accessory_image: UploadFile = File(...),
    prompt: str = Form(...)
):
    # ✅ Sauvegarde des images
    main_path = os.path.join(UPLOAD_DIR, main_image.filename)
    accessory_path = os.path.join(UPLOAD_DIR, accessory_image.filename)

    with open(main_path, "wb") as f:
        shutil.copyfileobj(main_image.file, f)
    with open(accessory_path, "wb") as f:
        shutil.copyfileobj(accessory_image.file, f)

    # ✅ Encodage base64
    def encode_image(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    base64_main = encode_image(main_path)
    base64_accessoire = encode_image(accessory_path)

    # ✅ Requête Gemini multimodal
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent"



    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": "ENTREZ VOTRE CLE"
    }
    

    data = {
    "contents": [
        {
        "parts": [
            {"text": prompt},
            {
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": base64_main
            }
            },
            {
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": base64_accessoire
            }
            }
        ]
        }
    ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    print(result)
    return response.json()

