from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    message: str

class PredictionResponse(BaseModel):
    classical_svm_confidence: float
    quantum_svm_confidence: float
    prediction: str
    inference_time_seconds: float
    is_mock: bool = False
