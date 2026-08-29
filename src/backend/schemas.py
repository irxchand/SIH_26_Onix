from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class HealthResponse(BaseModel):
    status: str
    message: str


class StudyStatus(str, Enum):
    READY = "READY"
    ANALYZING = "ANALYZING"
    COMPLETE = "COMPLETE"
    REVIEW = "REVIEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class StudyResponse(BaseModel):
    id: str
    patientId: str
    patientName: str
    age: int
    sex: str
    modality: str
    acquisitionDate: str
    status: StudyStatus
    imageUrl: str
    examDesc: Optional[str] = None
    issuesCount: Optional[int] = 0
    birads: Optional[str] = None
    referringPhysician: Optional[str] = None
    history: Optional[str] = None
    comments: Optional[str] = None
    attending: Optional[str] = None


class QueueResponse(BaseModel):
    studies: List[StudyResponse]
    total: int
    page: int


class UploadResponse(BaseModel):
    studyId: str
    status: StudyStatus
    imageUrl: str


class MetadataResponse(BaseModel):
    studyId: str
    pixelSpacingMm: float
    width: int
    height: int
    modality: str
    dicomTags: dict


class SegmentationResponse(BaseModel):
    studyId: str
    leftLung: Optional[str] = None
    rightLung: Optional[str] = None
    confidence: float


class EvidenceItem(BaseModel):
    id: str
    region: str
    confidence: float
    signal: str
    xPercent: float
    yPercent: float


class PredictionResponse(BaseModel):
    classical_svm_confidence: float
    quantum_svm_confidence: float
    prediction: str
    inference_time_seconds: float
    qubits: int = 8
    circuit_depth: int = 24
    runtime: float
    is_mock: bool = False
    feature_map: str = "ZZFeatureMap"
    simulator: str = "AerSimulator"
    execution_stage: str = "CACHED_BENCHMARK"
    evidence: List[EvidenceItem] = []


class Point(BaseModel):
    x: float
    y: float

class CalibrateRequest(BaseModel):
    brightness: int
    contrast: int
    sharpness: int

class MeasurementRequest(BaseModel):
    type: str
    points: List[Point]

    @classmethod
    def validate_ctr(cls, values):
        if values.get('type') == 'CTR' and len(values.get('points', [])) < 6:
            raise ValueError("CTR measurement requires at least 6 points")
        return values

class EvidenceRequest(BaseModel):
    region: str
    signal: str
    xPercent: float
    yPercent: float

class AnnotationRequest(BaseModel):
    path: str
    color: str

class StatusRequest(BaseModel):
    status: StudyStatus
