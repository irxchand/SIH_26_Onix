"""
SIH26139 — Anatomy-Grounded Hybrid Quantum AI Backend
Phase 2: Core Data Endpoints & Live Queue Integration
"""

import os
import time
import uuid
import shutil
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.backend.schemas import (
    HealthResponse,
    StudyResponse,
    StudyStatus,
    QueueResponse,
    UploadResponse,
    MetadataResponse,
    SegmentationResponse,
    PredictionResponse,
    EvidenceItem,
)

# ---------------------------------------------------------------------------
# In-memory study store (Phase 2: no database, kept in RAM)
# ---------------------------------------------------------------------------
STUDIES: dict[str, dict] = {}
UPLOADS_DIR = Path("data/uploads")

# Pre-seed the store with demonstration studies
_SEED_STUDIES = [
    {
        "id": "XR-2026-00421",
        "patientId": "PT-8802",
        "patientName": "Mariam Holden",
        "age": 55,
        "sex": "F",
        "modality": "CHEST X-RAY (PA)",
        "acquisitionDate": "29 AUG 2026 04:12",
        "status": StudyStatus.READY,
        "imageUrl": "http://localhost:8000/uploads/mock_xray_normal.jpg",
        "examDesc": "Chest X-ray",
        "issuesCount": 2,
        "birads": "2",
        "referringPhysician": "BORGES, Emilio",
        "history": "Heart attack, stroke on left side of brain",
        "comments": "Patient frequently complains of headaches, nausea, chest pains",
        "attending": "BORGES, Emilio",
    },
    {
        "id": "XR-2026-00512",
        "patientId": "PT-9410",
        "patientName": "Emmanuel Mack",
        "age": 62,
        "sex": "M",
        "modality": "CHEST X-RAY (PA)",
        "acquisitionDate": "29 AUG 2026 03:30",
        "status": StudyStatus.COMPLETE,
        "imageUrl": "http://localhost:8000/uploads/mock_xray_anomaly.jpg",
        "examDesc": "Abdominal X-ray",
        "issuesCount": 0,
        "birads": "1",
        "referringPhysician": "SMITH, John",
        "history": "None",
        "comments": "Routine checkup",
        "attending": "SMITH, John",
    },
    {
        "id": "XR-2026-00513",
        "patientId": "PT-2091",
        "patientName": "Ricardo Horton",
        "age": 48,
        "sex": "M",
        "modality": "CHEST X-RAY (AP)",
        "acquisitionDate": "29 AUG 2026 02:15",
        "status": StudyStatus.REVIEW,
        "imageUrl": "http://localhost:8000/uploads/mock_xray_anomaly2.jpg",
        "examDesc": "Venography",
        "issuesCount": 1,
        "birads": "3",
        "referringPhysician": "DAVIS, Alan",
        "history": "High blood pressure",
        "comments": "Patient reports dizziness",
        "attending": "DAVIS, Alan",
    },
    {
        "id": "XR-2026-00514",
        "patientId": "PT-1102",
        "patientName": "Sarah Davis",
        "age": 29,
        "sex": "F",
        "modality": "CHEST X-RAY (PA)",
        "acquisitionDate": "28 AUG 2026 19:40",
        "status": StudyStatus.READY,
        "imageUrl": "http://localhost:8000/uploads/mock_xray_normal2.jpg",
        "examDesc": "Chest X-ray",
        "issuesCount": 0,
        "birads": "1",
        "referringPhysician": "RODRIGUEZ, Maria",
        "history": "None",
        "comments": "No significant findings",
        "attending": "RODRIGUEZ, Maria",
    },
]


# ---------------------------------------------------------------------------
# Lifespan — runs once at startup, loads seed data and (eventually) ML models
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure upload directory exists
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    # Seed studies
    for s in _SEED_STUDIES:
        STUDIES[s["id"]] = s

    print(f"[STARTUP] Seeded {len(STUDIES)} studies into in-memory store.")
    print(f"[STARTUP] Upload directory: {UPLOADS_DIR.resolve()}")

    # Load pre-trained DenseNet121 model
    from src.ml.feature_extraction import DenseNetFeatureExtractor
    app.state.feature_extractor = DenseNetFeatureExtractor()
    print("[STARTUP] Pre-trained DenseNet121 weights loaded into memory.")

    # TODO Phase 3: Load PyTorch U-Net and Qiskit models here
    # from src.data.segmentation import UNetSegmenter
    # app.state.segmenter = UNetSegmenter()

    yield

    print("[SHUTDOWN] Cleaning up resources.")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SIH26139 Quantum AI Disease Detection API",
    description="Hybrid Quantum Machine Learning Platform for Early Disease Detection",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — allow the Next.js frontend on port 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images as static files
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR), check_dir=False), name="uploads")


# ===========================================================================
# ENDPOINTS
# ===========================================================================


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", message="API is running. Phase 2 active.")


# ---------------------------------------------------------------------------
# GET /api/v1/queue — paginated study list
# ---------------------------------------------------------------------------
@app.get("/api/v1/queue", response_model=QueueResponse)
async def get_queue(
    search: Optional[str] = Query(None, description="Filter by patient name or study ID"),
    status: Optional[str] = Query(None, description="Filter by study status"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    studies_list = list(STUDIES.values())

    # Filter by search term
    if search:
        q = search.lower()
        studies_list = [
            s for s in studies_list
            if q in s["patientName"].lower()
            or q in s["patientId"].lower()
            or q in s["id"].lower()
        ]

    # Filter by status
    if status:
        studies_list = [s for s in studies_list if s["status"] == status]

    total = len(studies_list)

    # Paginate
    start = (page - 1) * limit
    end = start + limit
    page_data = studies_list[start:end]

    return QueueResponse(
        studies=[StudyResponse(**s) for s in page_data],
        total=total,
        page=page,
    )


# ---------------------------------------------------------------------------
# POST /api/v1/upload — upload a CXR image
# ---------------------------------------------------------------------------
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB


@app.post("/api/v1/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    # Validate content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}. Only JPEG and PNG are accepted.",
        )

    # Read file and validate size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds 50MB limit.")

    # Generate study ID
    study_id = f"XR-UPLOAD-{uuid.uuid4().hex[:8].upper()}"
    ext = ".jpg" if file.content_type == "image/jpeg" else ".png"
    filename = f"{study_id}{ext}"
    filepath = UPLOADS_DIR / filename

    # Save file to disk
    with open(filepath, "wb") as f:
        f.write(content)

    # Create study record
    new_study = {
        "id": study_id,
        "patientId": f"PT-{uuid.uuid4().hex[:4].upper()}",
        "patientName": file.filename or "Uploaded Scan",
        "age": 0,
        "sex": "M",
        "modality": "IMPORTED CXR",
        "acquisitionDate": time.strftime("%d %b %Y %H:%M").upper(),
        "status": StudyStatus.READY,
        "imageUrl": f"http://localhost:8000/uploads/{filename}",
        "examDesc": "Imported X-ray",
        "issuesCount": 0,
        "birads": None,
        "referringPhysician": None,
        "history": None,
        "comments": "Uploaded via workstation",
        "attending": None,
    }

    STUDIES[study_id] = new_study

    return UploadResponse(
        studyId=study_id,
        status=StudyStatus.READY,
        imageUrl=new_study["imageUrl"],
    )


# ---------------------------------------------------------------------------
# GET /api/v1/studies/{id}/metadata
# ---------------------------------------------------------------------------
@app.get("/api/v1/studies/{study_id}/metadata", response_model=MetadataResponse)
async def get_metadata(study_id: str):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail=f"Study {study_id} not found.")

    study = STUDIES[study_id]

    # In Phase 3, this will read actual DICOM headers.
    # For now, return realistic mock metadata.
    return MetadataResponse(
        studyId=study_id,
        pixelSpacingMm=0.143,  # Typical CXR pixel spacing
        width=2048,
        height=2048,
        modality=study["modality"],
        dicomTags={
            "Manufacturer": "SHIMADZU",
            "InstitutionName": "SIH26139 Medical Center",
            "StudyDescription": study.get("examDesc", "CXR"),
            "PatientAge": str(study["age"]),
            "PatientSex": study["sex"],
        },
    )


# ---------------------------------------------------------------------------
# GET /api/v1/studies/{id}/segmentation
# ---------------------------------------------------------------------------
@app.get("/api/v1/studies/{study_id}/segmentation", response_model=SegmentationResponse)
async def get_segmentation(study_id: str):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail=f"Study {study_id} not found.")

    # In Phase 3, this will run the actual U-Net model.
    # For now, return realistic anatomical SVG contour paths.
    # These paths are normalized to the 0-100% coordinate space of the canvas.
    left_lung_path = (
        "M 20 25 C 16 18, 10 22, 8 38 "
        "C 6 54, 8 68, 12 78 "
        "C 16 85, 22 88, 28 85 "
        "C 32 78, 30 42, 20 25 Z"
    )
    right_lung_path = (
        "M 52 25 C 48 18, 42 22, 40 38 "
        "C 38 54, 40 68, 44 78 "
        "C 48 85, 54 88, 60 85 "
        "C 64 78, 62 42, 52 25 Z"
    )

    return SegmentationResponse(
        studyId=study_id,
        leftLung=left_lung_path,
        rightLung=right_lung_path,
        confidence=0.94,
    )


# ---------------------------------------------------------------------------
# POST /predict — (existing, expanded with full payload)
# ---------------------------------------------------------------------------
@app.get("/api/v1/studies/{study_id}/predict", response_model=PredictionResponse)
async def predict_study_get(study_id: str):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail=f"Study {study_id} not found.")
        
    start_time = time.time()
    time.sleep(0.3)  # Simulate processing
    inference_time = time.time() - start_time

    return PredictionResponse(
        classical_svm_confidence=0.87,
        quantum_svm_confidence=0.92,
        prediction="Anomaly Detected" if "anomaly" in STUDIES[study_id].get("imageUrl", "") else "Healthy",
        inference_time_seconds=inference_time,
        is_mock=True,
        qubits=8,
        circuit_depth=16,
        runtime=inference_time,
        feature_map="ZZFeatureMap",
        simulator="AerSimulator",
        execution_stage="CACHED_BENCHMARK",
        evidence=[
            EvidenceItem(
                id="E-01",
                region="RIGHT LOWER LUNG LOBE",
                confidence=0.87,
                signal="Abnormal density/feature pattern detected in right lower zone",
                xPercent=38,
                yPercent=68,
            )
        ]
    )

@app.post("/predict", response_model=PredictionResponse)
@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    start_time = time.time()

    # TODO Phase 3: Run actual PyTorch -> PCA -> QSVM pipeline
    time.sleep(0.3)  # Simulate processing

    inference_time = time.time() - start_time

    return PredictionResponse(
        classical_svm_confidence=0.87,
        quantum_svm_confidence=0.92,
        prediction="Anomaly Detected",
        inference_time_seconds=inference_time,
        is_mock=True,
        qubits=8,
        circuit_depth=16,
        runtime=inference_time,
        feature_map="ZZFeatureMap",
        simulator="AerSimulator",
        execution_stage="CACHED_BENCHMARK",
        evidence=[
            EvidenceItem(
                id="E-01",
                region="RIGHT LOWER LUNG LOBE",
                confidence=0.87,
                signal="Abnormal density/feature pattern detected in right lower zone",
                xPercent=38,
                yPercent=68,
            )
        ]
    )
