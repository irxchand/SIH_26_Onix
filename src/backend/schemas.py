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
    dataset: Optional[str] = None
    trueLabel: Optional[str] = None


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
    goldStandard: Optional[str] = None
    clinicalReading: Optional[str] = None
    verificationSource: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None


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
    note: Optional[str] = None


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
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    reasoning: Optional[ReasoningResponse] = None

class MeasurementPointRequest(BaseModel):
    x: int
    y: int
    
class ChecklistItemRequest(BaseModel):
    id: str
    label: str
    status: str
    point: Optional[MeasurementPointRequest] = None

class MeasurementRequest(BaseModel):
    points: List[ChecklistItemRequest]
    hDistMm: float
    cDistMm: float
    ratio: float
    note: Optional[str] = None

class CalibrateRequest(BaseModel):
    brightness: int
    contrast: int
    sharpness: int

class EvidenceNotesRequest(BaseModel):
    id: str
    note: str
    xPercent: float
    yPercent: float

class BoundingBox(BaseModel):
    id: str
    label: str
    x: float
    y: float
    width: float
    height: float

class AnnotationRequest(BaseModel):
    global_tags: List[str]
    boxes: List[BoundingBox]

class StatusRequest(BaseModel):
    status: StudyStatus

class ReportRequest(BaseModel):
    prompt: str


class FindingItem(BaseModel):
    id: str = "E01"
    region: str
    finding: str
    severity: str = "HIGH"
    confidence: float = 0.85
    source: str = "LLM_ASSISTED_PROTOTYPE"
    signal: Optional[str] = None
    xPercent: Optional[float] = None
    yPercent: Optional[float] = None
    note: Optional[str] = None


class AnnotationBox(BaseModel):
    id: Optional[str] = "E01"
    x: float
    y: float
    width: float
    height: float
    label: str
    confidence: Optional[float] = 0.85
    color: Optional[str] = "#EF4444"


class ComparisonData(BaseModel):
    classical_prediction: str
    quantum_prediction: str
    classical_score: Optional[float] = None
    quantum_score: Optional[float] = None


class ReasoningResponse(BaseModel):
    overall_assessment: str
    findings: List[FindingItem]
    annotations: List[AnnotationBox]
    comparison: ComparisonData
    limitations: List[str]
    disclaimer: str
    provenance: Optional[str] = "LLM_ASSISTED_PROTOTYPE"

