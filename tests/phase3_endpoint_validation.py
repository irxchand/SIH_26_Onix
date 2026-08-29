import io
import pytest
from fastapi.testclient import TestClient
from src.backend.main import app

def test_calibrate_endpoint():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/studies/XR-2026-00421/calibrate",
            json={"brightness": 120, "contrast": 110, "sharpness": 50}
        )
        assert response.status_code == 200

def test_measurement_endpoint_valid():
    with TestClient(app) as client:
        # Dharmit's schema requires points of ChecklistItemRequest, hDistMm, cDistMm, ratio
        points = [
            {"id": str(i), "label": f"Point {i}", "status": "active", "point": {"x": i, "y": i}} 
            for i in range(6)
        ]
        response = client.post(
            "/api/v1/studies/XR-2026-00421/measurements",
            json={
                "points": points,
                "hDistMm": 150.0,
                "cDistMm": 300.0,
                "ratio": 0.5,
                "note": "Normal CTR"
            }
        )
        assert response.status_code == 200

def test_measurement_endpoint_invalid_ctr():
    with TestClient(app) as client:
        # Invalid has < 6 points
        points = [
            {"id": str(i), "label": f"Point {i}", "status": "active", "point": {"x": i, "y": i}} 
            for i in range(5)
        ]
        response = client.post(
            "/api/v1/studies/XR-2026-00421/measurements",
            json={
                "points": points,
                "hDistMm": 150.0,
                "cDistMm": 300.0,
                "ratio": 0.5
            }
        )
        assert response.status_code == 422

def test_evidence_endpoint():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/studies/XR-2026-00421/evidence",
            json={"note": "Possible nodule in left upper lobe", "xPercent": 50.0, "yPercent": 50.0}
        )
        assert response.status_code == 200

def test_annotations_endpoint():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/studies/XR-2026-00421/annotations",
            json={"paths": ["M10 10 L20 20"]}
        )
        assert response.status_code == 200

def test_status_endpoint():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/studies/XR-2026-00421/status",
            json={"status": "REVIEW"}
        )
        assert response.status_code == 200

def test_predict_endpoint_ml_pipeline():
    with TestClient(app) as client:
        # This will test the live PyTorch -> PCA -> QSVM pipeline
        response = client.get("/api/v1/studies/XR-2026-00421/predict")
        assert response.status_code == 200
        data = response.json()
        assert data["is_mock"] is False
        assert data["execution_stage"] == "QSVM_EVALUATION"
