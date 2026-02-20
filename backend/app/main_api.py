import sys
import os

# Add the backend directory to the python path so we can import app modules
# This resolves the "ModuleNotFoundError: No module named 'app'"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Sherlock Deepfake Detection API",
    description="API for detecting visual and audio manipulations in media files.",
    version="1.0.0"
)

# CORS (Cross-Origin Resource Sharing)
# Allow requests from everywhere for development. Restrict in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Sherlock Deepfake Detection System is Online"}

def start():
    """Launched with `poetry run start` or `python backend/main_api.py`"""
    uvicorn.run("app.main_api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()

