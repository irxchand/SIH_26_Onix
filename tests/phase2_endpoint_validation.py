from fastapi.testclient import TestClient
from src.backend.main import app
import io

client = TestClient(app)

def test_queue_endpoint():
    response = client.get("/api/v1/queue")
    # Will fail until endpoint is implemented
    assert response.status_code == 200, "Queue endpoint should return 200 OK"
    data = response.json()
    assert isinstance(data, list), "Queue should return a list of studies"

def test_upload_endpoint():
    dummy_file = io.BytesIO(b"dummy image data")
    response = client.post(
        "/api/v1/upload", 
        files={"file": ("test.png", dummy_file, "image/png")}
    )
    assert response.status_code == 200, "Upload endpoint should return 200 OK"
    data = response.json()
    assert "study_id" in data, "Upload response should include a study_id"

def test_metadata_endpoint():
    # Use a dummy ID
    response = client.get("/api/v1/studies/123/metadata")
    assert response.status_code == 200, "Metadata endpoint should return 200 OK"

def test_segmentation_endpoint():
    response = client.get("/api/v1/studies/123/segmentation")
    assert response.status_code == 200, "Segmentation endpoint should return 200 OK"

def test_predict_endpoint_payload():
    dummy_file = io.BytesIO(b"dummy image data")
    response = client.post(
        "/predict", 
        files={"file": ("test.png", dummy_file, "image/png")}
    )
    assert response.status_code == 200, "Predict endpoint should return 200 OK"
    data = response.json()
    assert "qubits" in data, "Response missing qubits tracking"
    assert "circuit_depth" in data, "Response missing circuit_depth tracking"
    assert "runtime" in data, "Response missing runtime tracking"

