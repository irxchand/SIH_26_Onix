from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import json
import base64
from pathlib import Path


class LLMAnnotationItem(BaseModel):
    id: str = "E01"
    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)
    width: float = Field(default=0.15, ge=0.0, le=1.0)
    height: float = Field(default=0.15, ge=0.0, le=1.0)
    region: str
    finding: str
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    display: bool = True


class LLMReasoningOutput(BaseModel):
    prediction: str
    classical_score: float = Field(ge=0.0, le=1.0)
    quantum_score: float = Field(ge=0.0, le=1.0)
    consensus: str
    show_evidence: bool
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)
    annotations: List[LLMAnnotationItem] = []
    reasoning_summary: str
    report_summary: str
    limitations: List[str] = []
    provenance: str = "LLM_ASSISTED_PROTOTYPE"


class BaseLLMProvider(ABC):
    """Abstract interface for LLM-assisted prototype reasoning."""

    def __init__(self, prompt_file: Optional[str] = None):
        if prompt_file and Path(prompt_file).exists():
            self.system_prompt = Path(prompt_file).read_text()
        else:
            default_prompt = Path("src/backend/prompts/level_c_reasoning_prompt.txt")
            if default_prompt.exists():
                self.system_prompt = default_prompt.read_text()
            else:
                self.system_prompt = "You are a research prototype reasoning assistant for chest X-ray QML analysis."

    def prepare_multimodal_payload(self, image_path: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Packages the multimodal payload with image reference, base64 visual stream, and context."""
        img_b64 = self.encode_image_base64(image_path)
        return {
            "system_prompt": self.system_prompt,
            "image_attachment": {
                "path": str(image_path),
                "has_data": img_b64 is not None,
                "base64_preview": f"{img_b64[:30]}..." if img_b64 else None
            },
            "structured_context": context,
            "response_format": {"type": "json_object"}
        }

    def encode_image_base64(self, image_path: str) -> Optional[str]:
        """Reads the actual image file and encodes it as base64 string for multimodal ingestion."""
        p = Path(image_path)
        if not p.exists():
            return None
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def validate_and_parse_response(self, raw_response: str) -> LLMReasoningOutput:
        """Strictly validates that LLM returned compliant structured JSON."""
        cleaned = raw_response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)
        return LLMReasoningOutput(**data)

    @abstractmethod
    def analyze(self, image_path: str, context: Dict[str, Any]) -> LLMReasoningOutput:
        """Dispatches actual image + structured Level B context to the reasoning engine."""
        pass
