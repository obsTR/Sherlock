from pydantic import BaseModel
from typing import Optional, Dict

class AnalysisResponse(BaseModel):
    filename: str
    is_fake: bool
    confidence: float
    fake_probability: float
    details: Dict[str, Optional[float]]
    processing_time: float

class ErrorResponse(BaseModel):
    error: str



