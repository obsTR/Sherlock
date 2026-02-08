from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import time
from pathlib import Path
from app.core.detector import DeepfakeDetector
from app.api.schemas import AnalysisResponse, ErrorResponse

router = APIRouter()

# Initialize detector once (singleton pattern effectively)
# In production, we might use dependency injection or lifespan events
detector = DeepfakeDetector()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_video(file: UploadFile = File(...)):
    """
    Upload a video file and analyze it for deepfake artifacts.
    """
    start_time = time.time()
    
    # 1. Save uploaded file
    try:
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    
    # 2. Run Analysis
    try:
        # The detector is synchronous, so this might block the event loop.
        # For high-concurrency, this should run in a threadpool (FastAPI does this for def functions)
        # or use run_in_executor.
        result = detector.analyze_video(str(file_path))
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            filename=result["file"],
            is_fake=result["is_fake"],
            confidence=result["confidence"],
            fake_probability=result["fake_probability"],
            details={
                "visual_prob": result["details"].get("visual_prob"),
                "audio_prob": result["details"].get("audio_prob"),
                "frames_analyzed": float(result["details"].get("frames_analyzed", 0))
            },
            processing_time=round(processing_time, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Clean up file in case of crash? Maybe keep for debugging.
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")
    finally:
        # Optional: Cleanup uploaded file to save space
        # if file_path.exists():
        #     os.remove(file_path)
        pass



