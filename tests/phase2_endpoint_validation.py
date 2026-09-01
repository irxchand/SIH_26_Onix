from fastapi.testclient import TestClient
from src.backend.main import app
import io

def test_queue_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/v1/queue")
        assert response.status_code == 200, "Queue endpoint should return 200 OK"
        data = response.json()
        assert "studies" in data, "Queue response missing 'studies' key"
        assert isinstance(data["studies"], list), "Queue should return a list of studies"

def test_upload_endpoint():
    dummy_file = io.BytesIO(b"dummy image data")
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/upload", 
            files={"file": ("test.png", dummy_file, "image/png")}
        )
        assert response.status_code == 200, "Upload endpoint should return 200 OK"
        data = response.json()
        assert "studyId" in data, "Upload response missing studyId"

def test_metadata_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/v1/studies/XR-2026-00421/metadata")
        assert response.status_code == 200, "Metadata endpoint should return 200 OK"

def test_segmentation_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/v1/studies/XR-2026-00421/segmentation")
        assert response.status_code == 200, "Segmentation endpoint should return 200 OK"

def test_predict_endpoint_payload():
    with TestClient(app) as client:
        # Test new GET prediction logic for existing study
        response = client.get("/api/v1/studies/XR-2026-00421/predict")
        assert response.status_code == 200, "Predict endpoint should return 200 OK"
        data = response.json()
        assert "qubits" in data, "Response missing qubits tracking"
        assert "circuit_depth" in data, "Response missing circuit_depth tracking"
        assert "runtime" in data, "Response missing runtime tracking"
