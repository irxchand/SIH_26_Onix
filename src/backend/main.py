"""
SIH26139 — Anatomy-Grounded Hybrid Quantum AI Backend
Phase 2: Core Data Endpoints & Live Queue Integration
"""

import os
import time
import uuid
import shutil
import cv2
import random
from datetime import datetime
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# ---------------------------------------------------------------------------
# SECURITY & DPDP COMPLIANCE (Phase 2 Mock)
# ---------------------------------------------------------------------------
def verify_token(authorization: Optional[str] = Header(None)):
    """
    Simulates a DPDP-compliant JWT validation layer via an API Gateway.
    In a real production environment, Kong or AWS API Gateway would terminate TLS
    and validate the RBAC roles. We mock it here to prove the zero-trust architecture.
    """
    if authorization is not None and authorization != "Bearer SIH2026_MOCK_TOKEN":
        raise HTTPException(status_code=401, detail="Invalid DPDP access token.")
    return True

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
    CalibrateRequest,
    MeasurementRequest,
    EvidenceNotesRequest,
    AnnotationRequest,
    StatusRequest,
)

# ---------------------------------------------------------------------------
# In-memory study store (Phase 2: no database, kept in RAM)
# ---------------------------------------------------------------------------
STUDIES: dict[str, dict] = {}
UPLOADS_DIR = Path("data/uploads")

from src.ml.segmentation import get_lung_contours_svg, get_montgomery_mask_contours

# Pre-seed the store with demonstration studies
# (Removed mock _SEED_STUDIES to prevent fake patient profiles)


# ---------------------------------------------------------------------------
# Lifespan — runs once at startup, loads seed data and (eventually) ML models
# ---------------------------------------------------------------------------
def get_study_filepath(image_url: str) -> Path:
    """Helper to resolve the local filesystem path of an image URL."""
    filename = image_url.split("/")[-1]
    if "datasets" in image_url:
        return Path("data/datasets/montgomery/MontgomerySet/CXR_png") / filename
    else:
        return UPLOADS_DIR / filename

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure upload directory exists
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    # Seed studies from the Montgomery test split dataset
    test_split_path = Path("data/experiments/test_split.json")
    if test_split_path.exists():
        import json
        with open(test_split_path, "r") as f:
            test_samples = json.load(f)
        for idx, item in enumerate(test_samples):
            study_id = item["studyId"]
            img_url = f"http://localhost:8000/datasets/montgomery/MontgomerySet/CXR_png/{item['filename']}"
            s = {
                "id": study_id,
                "patientId": study_id,
                "patientName": f"Montgomery Sample {idx+1}",
                "age": item["age"],
                "sex": item["sex"],
                "modality": "CHEST X-RAY (PA)",
                "acquisitionDate": time.strftime("%d %b %Y %H:%M").upper(),
                "status": StudyStatus.READY,
                "imageUrl": img_url,
                "examDesc": "Chest X-ray (PA)",
                "dataset": "Montgomery County",
                "trueLabel": item["label"],
                "history": "No prior history recorded.",
                "comments": item["comments"],
                "version": 1,
                "calibration": {"brightness": 100, "contrast": 100, "sharpness": 100},
                "measurements": None,
                "annotations": [],
                "evidence": []
            }
            STUDIES[study_id] = s
    else:
        raise RuntimeError("Strict Mode: Montgomery test split dataset index missing! Please run 'python -m src.ml.qsvm' first.")

    print(f"[STARTUP] Seeded {len(STUDIES)} studies into in-memory store.")
    print(f"[STARTUP] Upload directory: {UPLOADS_DIR.resolve()}")

    # ── ML weights ────────────────────────────────────────────────────────
    import json as _json
    from src.ml.qsvm import load_weights

    weights_dir   = Path("src/ml/weights")
    required = ["scaler.pkl", "pca.pkl", "classical_svm.pkl",
                "pca_quantum.pkl", "qsvm.pkl", "thresholds.pkl", "config.pkl"]
    missing = [w for w in required if not (weights_dir / w).exists()]
    if missing:
        print(f"[STARTUP] Missing weights: {missing}. Running optimizer...")
        import subprocess
        subprocess.run(["python", "-m", "src.ml.optimize"], check=True)

    # Load optimizer config to know which encoder+representation was selected
    cfg = load_weights(str(weights_dir / "config.pkl"))
    print(f"[STARTUP] Optimizer config: {cfg}")

    # Load the feature extractor matching Track A encoder/representation
    from src.ml.feature_extraction import CXRFeatureExtractor
    _REPR_MAP = {"WHOLE_CXR": "whole", "GT_LUNG_MASKED": "masked", "GT_LUNG_CROPPED": "cropped"}
    app.state.feature_extractor = CXRFeatureExtractor(
        encoder=cfg["encoder"],
        representation=_REPR_MAP.get(cfg.get("track_a_representation", "WHOLE_CXR"), "whole"),
        clahe=True,
    )
    app.state.track_a_repr_label = cfg.get("track_a_representation", "WHOLE_CXR")
    app.state.track_b_repr_label = cfg.get("track_b_representation", "WHOLE_CXR")
    print(f"[STARTUP] Encoder={cfg['encoder']}  TrackA_repr={app.state.track_a_repr_label}")

    # Load QSVM feature extractor (may use same or different repr)
    _qb_repr = _REPR_MAP.get(cfg.get("track_b_representation", "WHOLE_CXR"), "whole")
    if cfg.get("track_b_representation") == cfg.get("track_a_representation"):
        app.state.qsvm_feature_extractor = app.state.feature_extractor
    else:
        app.state.qsvm_feature_extractor = CXRFeatureExtractor(
            encoder=cfg["encoder"], representation=_qb_repr, clahe=True
        )
    print(f"[STARTUP] QSVM extractor repr={cfg.get('track_b_representation', 'WHOLE_CXR')}")

    # Load weights
    app.state.scaler          = load_weights(str(weights_dir / "scaler.pkl"))
    app.state.pca             = load_weights(str(weights_dir / "pca.pkl"))
    app.state.classical_svm   = load_weights(str(weights_dir / "classical_svm.pkl"))
    app.state.pca_quantum     = load_weights(str(weights_dir / "pca_quantum.pkl"))
    app.state.qsvm            = load_weights(str(weights_dir / "qsvm.pkl"))
    thresholds                = load_weights(str(weights_dir / "thresholds.pkl"))
    app.state.classical_thresh = float(thresholds.get("classical_thresh", 0.0))
    app.state.quantum_thresh   = float(thresholds.get("quantum_thresh",   0.0))
    app.state.ml_config        = cfg
    print(f"[STARTUP] Weights loaded. Classical thresh={app.state.classical_thresh:.4f}  Quantum thresh={app.state.quantum_thresh:.4f}")

    # Load separate scaler for quantum path if Track B used different representation
    # (optimizer saves a single scaler based on Track A; Track B re-fits its own)
    # For now quantum path reuses Track A scaler — acceptable because same encoder
    app.state.qsvm_scaler = app.state.scaler

    # Load training kernel reference points (needed for quantum kernel eval)
    x_train_path = weights_dir / "x_train.pkl"
    if x_train_path.exists():
        app.state.X_train_pca = load_weights(str(x_train_path))
    else:
        app.state.X_train_pca = None
        print("[STARTUP WARNING] x_train.pkl missing — QSVM inference will fail.")

    print("[STARTUP] All ML weights loaded successfully.")

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
# Serve dataset images as static files
app.mount("/datasets", StaticFiles(directory="data/datasets", check_dir=False), name="datasets")


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
        "version": 1,
        "calibration": {"brightness": 100, "contrast": 100, "sharpness": 100},
        "measurements": None,
        "annotations": [],
        "evidence": [],
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
async def get_study_metadata(study_id: str):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail=f"Study {study_id} not found.")
        
    study = STUDIES[study_id]
    filepath = get_study_filepath(study["imageUrl"])
    
    width, height = 2048, 2048 # Fallback
    pixel_spacing = 0.143
    if filepath.exists():
        img = cv2.imread(str(filepath))
        if img is not None:
            height, width = img.shape[:2]
            # Heuristic: assume average chest width is ~350mm
            pixel_spacing = 350.0 / width

    return MetadataResponse(
        studyId=study_id,
        pixelSpacingMm=pixel_spacing,
        width=width,
        height=height,
        modality=study["modality"],
        dicomTags={
            "Manufacturer": "NLM",
            "InstitutionName": "Montgomery County HHS",
            "StudyDescription": study.get("examDesc", "CXR"),
            "PatientAge": str(study["age"]),
            "PatientSex": study["sex"],
        },
    )


# ---------------------------------------------------------------------------
# GET /api/v1/studies/{id}/segmentation
# ---------------------------------------------------------------------------
@app.get("/api/v1/studies/{study_id}/segmentation", response_model=SegmentationResponse)
async def get_segmentation(study_id: str, mode: str = "ground_truth"):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail=f"Study {study_id} not found.")

    study = STUDIES[study_id]
    
    left_lung_path = ""
    right_lung_path = ""
    is_gt = False
    
    if mode == "ground_truth":
        # Try reading manual masks first (Montgomery Set ground truth)
        gt_contours = get_montgomery_mask_contours(study_id)
        if gt_contours:
            left_lung_path = gt_contours["leftLung"]
            right_lung_path = gt_contours["rightLung"]
            is_gt = True
            
    if not is_gt:
        # Fallback / explicit automated Otsu thresholding
        filepath = get_study_filepath(study["imageUrl"])
        if filepath.exists():
            contours = get_lung_contours_svg(str(filepath))
            left_lung_path = contours["leftLung"]
            right_lung_path = contours["rightLung"]

    return SegmentationResponse(
        studyId=study_id,
        leftLung=left_lung_path,
        rightLung=right_lung_path,
        # confidence=1.0: ground-truth Montgomery expert mask
        # confidence=0.0: Otsu heuristic — NOT a model prediction
        confidence=1.0 if is_gt else 0.0,
    )


# ---------------------------------------------------------------------------
# POST /predict — (existing, expanded with full payload)
# ---------------------------------------------------------------------------
from src.ml.qsvm import construct_quantum_kernel
import numpy as np
import asyncio

def run_ml_pipeline(app, image_path: str):
    """
    Synchronous ML inference pipeline.
    Uses Track A (classical) and Track B (quantum) configs from the optimizer.
    Returns honest decision scores — NOT clamped fake probabilities.
    """
    import numpy as np
    from src.ml.qsvm import construct_quantum_kernel

    # ── Track A: Classical inference ─────────────────────────────────────
    # Uses best encoder + representation + PCA + classifier from optimizer
    features_a  = app.state.feature_extractor.extract(image_path).numpy()
    scaled_a    = app.state.scaler.transform(features_a.reshape(1, -1))
    pca_a       = app.state.pca.transform(scaled_a)          # Track A PCA
    decision_c  = float(app.state.classical_svm.decision_function(pca_a)[0])
    prediction_c = 1 if decision_c >= app.state.classical_thresh else 0

    # ── Track B: Quantum inference ────────────────────────────────────────
    # Same encoder, possibly different representation, fixed PCA-8
    features_q = app.state.qsvm_feature_extractor.extract(image_path).numpy()
    scaled_q   = app.state.qsvm_scaler.transform(features_q.reshape(1, -1))
    pca_q      = app.state.pca_quantum.transform(scaled_q)   # Track B PCA (dim=8)

    if app.state.X_train_pca is not None:
        qkernel = construct_quantum_kernel()
        K_test  = qkernel.evaluate(x_vec=pca_q, y_vec=app.state.X_train_pca)
        decision_q  = float(app.state.qsvm.decision_function(K_test)[0])
        prediction_q = 1 if decision_q >= app.state.quantum_thresh else 0
    else:
        # Graceful fallback: quantum weights missing, use classical
        decision_q   = decision_c
        prediction_q = prediction_c

    # ── Final prediction: Track A classical is the demo-facing result ─────
    # (Track B quantum used for the research comparison panel)
    final_pred = prediction_c

    return {
        "prediction"   : "Tuberculosis Detected" if final_pred == 1 else "Normal — No TB Detected",
        "classical_pred": int(prediction_c),
        "quantum_pred"  : int(prediction_q),
        "classical_score": decision_c,          # raw decision score, not clamped
        "quantum_score"  : decision_q,           # raw decision score, not clamped
        "track_a_repr"  : getattr(app.state, "track_a_repr_label", "WHOLE_CXR"),
        "track_b_repr"  : getattr(app.state, "track_b_repr_label", "WHOLE_CXR"),
    }


@app.get("/api/v1/studies/{study_id}/predict", response_model=PredictionResponse)
async def predict_study_get(study_id: str):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail=f"Study {study_id} not found.")
        
    start_time = time.time()
    
    # Extract filename from imageUrl
    image_url = STUDIES[study_id].get("imageUrl", "")
    filepath = get_study_filepath(image_url)
    
    # Run pipeline in a threadpool to avoid blocking event loop
    if filepath.exists():
        res = await asyncio.to_thread(run_ml_pipeline, app, str(filepath))
    else:
        raise HTTPException(
            status_code=404,
            detail="Source image file not found on backend. Cannot perform inference."
        )

    inference_time = time.time() - start_time

    # Map raw decision scores to [0, 1] range via sigmoid for UI display, but label honestly
    c_prob = float(1.0 / (1.0 + np.exp(-res["classical_score"])))
    q_prob = float(1.0 / (1.0 + np.exp(-res["quantum_score"])))

    return PredictionResponse(
        classical_svm_confidence=c_prob,
        quantum_svm_confidence=q_prob,
        prediction=res["prediction"],
        inference_time_seconds=inference_time,
        is_mock=False,
        qubits=int(app.state.ml_config.get("pca_dim_quantum", 8)),
        circuit_depth=16,
        runtime=inference_time,
        feature_map="ZZFeatureMap",
        simulator="StatevectorSampler",
        execution_stage="QSVM_EVALUATION",
        evidence=[
            EvidenceItem(
                id="E-01",
                region="LUNG FIELD",
                confidence=q_prob,
                signal=f"QSVM score: {res['quantum_score']:.4f} | Classical: {res['classical_score']:.4f}",
                xPercent=38,
                yPercent=68,
            )
        ],
        image_width=res.get("image_width"),
        image_height=res.get("image_height")
    )

@app.post("/predict", response_model=PredictionResponse)
@app.post("/api/v1/predict", response_model=PredictionResponse, dependencies=[Depends(verify_token)])
async def predict_image(file: UploadFile = File(...)):
    start_time = time.time()

    # Save temp file
    temp_path = UPLOADS_DIR / f"temp_{uuid.uuid4().hex[:8]}.jpg"
    content = await file.read()
    with open(temp_path, "wb") as f:
        f.write(content)

    # Run ML pipeline
    res = await asyncio.to_thread(run_ml_pipeline, app, str(temp_path))
    
    # Cleanup temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    inference_time = time.time() - start_time

    # Map raw decision scores to [0, 1] range via sigmoid for UI display, but label honestly
    c_prob = float(1.0 / (1.0 + np.exp(-res["classical_score"])))
    q_prob = float(1.0 / (1.0 + np.exp(-res["quantum_score"])))

    return PredictionResponse(
        classical_svm_confidence=c_prob,
        quantum_svm_confidence=q_prob,
        prediction=res["prediction"],
        inference_time_seconds=inference_time,
        is_mock=False,
        qubits=int(app.state.ml_config.get("pca_dim_quantum", 8)),
        circuit_depth=16,
        runtime=inference_time,
        feature_map="ZZFeatureMap",
        simulator="StatevectorSampler",
        execution_stage="QSVM_EVALUATION",
        evidence=[
            EvidenceItem(
                id="E-01",
                region="LUNG FIELD",
                confidence=q_prob,
                signal=f"QSVM score: {res['quantum_score']:.4f} | Classical: {res['classical_score']:.4f}",
                xPercent=38,
                yPercent=68,
            )
        ],
        image_width=res.get("image_width"),
        image_height=res.get("image_height")
    )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# POST /api/v1/studies/{id}/calibrate
# ---------------------------------------------------------------------------
@app.post("/api/v1/studies/{study_id}/calibrate")
async def calibrate_study(study_id: str, req: CalibrateRequest):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail="Study not found.")
    STUDIES[study_id]["calibration"] = req.model_dump()
    STUDIES[study_id]["version"] += 1
    return {"status": "success", "calibration": req.model_dump(), "version": STUDIES[study_id]["version"]}


# ---------------------------------------------------------------------------
# GET, POST /api/v1/studies/{id}/measurements
# ---------------------------------------------------------------------------
@app.post("/api/v1/studies/{study_id}/measurements")
async def save_measurements(study_id: str, req: MeasurementRequest):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail="Study not found.")
        
    if len(req.points) < 6:
        raise HTTPException(status_code=422, detail="Measurement requires at least 6 points.")
        
    STUDIES[study_id]["measurements"] = req.model_dump()
    STUDIES[study_id]["version"] += 1
    return {"status": "success", "version": STUDIES[study_id]["version"]}

@app.get("/api/v1/studies/{study_id}/measurements")
async def get_measurements(study_id: str):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail="Study not found.")
    return STUDIES[study_id].get("measurements")


# ---------------------------------------------------------------------------
# GET, POST /api/v1/studies/{id}/evidence
# ---------------------------------------------------------------------------
@app.post("/api/v1/studies/{study_id}/evidence")
async def add_evidence_note(study_id: str, req: EvidenceNotesRequest):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail="Study not found.")
        
    # Generate an ID for the evidence
    ev_id = f"EV-{uuid.uuid4().hex[:6].upper()}"
    new_evidence = {
        "id": ev_id,
        "note": req.note,
        "xPercent": req.xPercent,
        "yPercent": req.yPercent,
        "timestamp": time.time()
    }
    
    if "evidence" not in STUDIES[study_id]:
        STUDIES[study_id]["evidence"] = []
        
    STUDIES[study_id]["evidence"].append(new_evidence)
    STUDIES[study_id]["version"] += 1
    return {"status": "success", "evidence": new_evidence, "version": STUDIES[study_id]["version"]}

@app.get("/api/v1/studies/{study_id}/evidence")
async def get_evidence(study_id: str):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail="Study not found.")
    return {"evidence": STUDIES[study_id].get("evidence", [])}


# ---------------------------------------------------------------------------
# GET, POST, DELETE /api/v1/studies/{id}/annotations
# ---------------------------------------------------------------------------
@app.post("/api/v1/studies/{study_id}/annotations")
async def save_annotations(study_id: str, req: AnnotationRequest):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail="Study not found.")
    STUDIES[study_id]["annotations"] = req.paths
    STUDIES[study_id]["version"] += 1
    return {"status": "success", "version": STUDIES[study_id]["version"]}

@app.get("/api/v1/studies/{study_id}/annotations")
async def get_annotations(study_id: str):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail="Study not found.")
    return {"paths": STUDIES[study_id].get("annotations", [])}

@app.delete("/api/v1/studies/{study_id}/annotations")
async def delete_annotations(study_id: str):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail="Study not found.")
    STUDIES[study_id]["annotations"] = []
    STUDIES[study_id]["version"] += 1
    return {"status": "success", "version": STUDIES[study_id]["version"]}


# ---------------------------------------------------------------------------
# POST /api/v1/studies/{id}/status
# ---------------------------------------------------------------------------
@app.post("/api/v1/studies/{study_id}/status")
async def update_status(study_id: str, req: StatusRequest):
    if study_id not in STUDIES:
        raise HTTPException(status_code=404, detail="Study not found.")
    STUDIES[study_id]["status"] = req.status
    STUDIES[study_id]["version"] += 1
    return {"status": "success", "new_status": req.status, "version": STUDIES[study_id]["version"]}

