from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import time

from src.backend.schemas import PredictionResponse, HealthResponse

app = FastAPI(
    title="Quantum AI Disease Detection API",
    description="Hybrid Quantum Machine Learning Platform for Early Disease Detection",
    version="1.0.0"
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", message="API is running.")

@app.post("/predict", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    # This is a mock response for Phase 1. 
    # In Phase 2/3, this will route to PyTorch U-Net -> DenseNet -> QSVM.
    start_time = time.time()
    
    # Fake processing time
    time.sleep(0.5)
    
    inference_time = time.time() - start_time
    
    return PredictionResponse(
        classical_svm_confidence=0.87,
        quantum_svm_confidence=0.92,
        prediction="Anomaly Detected",
        inference_time_seconds=inference_time,
        is_mock=True
    )
