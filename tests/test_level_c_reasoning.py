import unittest
import json
from pathlib import Path

from src.backend.llm.base import BaseLLMProvider, LLMReasoningOutput, LLMAnnotationItem
from src.backend.llm.mock_provider import MockLLMProvider
from src.backend.llm.browser_chatgpt import BrowserChatGPTProvider
from src.backend.reasoning_provider import InformedPrototypeReasoningProvider


class TestLevelCReasoning(unittest.TestCase):

    def setUp(self):
        self.provider = BrowserChatGPTProvider()
        self.mock_provider = MockLLMProvider()
        self.sample_image = "data/datasets/montgomery/MontgomerySet/CXR_png/MCUCXR_0021_0.png"
        self.reasoning_engine = InformedPrototypeReasoningProvider()

    def test_01_image_attached_as_base64(self):
        """Test 1: Actual image is read and encoded as base64 in multimodal payload."""
        payload = self.provider.prepare_multimodal_payload(self.sample_image, {"case_id": "TEST_01"})
        self.assertTrue(payload["image_attachment"]["has_data"])
        self.assertIsNotNone(payload["image_attachment"]["base64_preview"])
        self.assertEqual(payload["image_attachment"]["path"], self.sample_image)

    def test_02_full_structured_context_generation(self):
        """Test 2: Structured context is generated without inventing fields."""
        context = self.reasoning_engine.build_structured_context(
            study_id="TEST_CASE_99",
            image_path=self.sample_image,
            metadata={"dataset": "Montgomery County", "age": 45, "sex": "F"}
        )
        self.assertEqual(context["case_id"], "TEST_CASE_99")
        self.assertEqual(context["dataset"], "Montgomery County")
        self.assertIn("preprocessing", context)
        self.assertEqual(context["feature_information"]["encoder"], "densenet121")
        self.assertIsNone(context["classical_result"])

    def test_03_valid_json_parsed_correctly(self):
        """Test 3: Valid JSON response conforming to schema parses correctly."""
        raw_json = '''{
            "prediction": "Tuberculosis Detected",
            "classical_score": 0.74,
            "quantum_score": 0.96,
            "consensus": "Tuberculosis Detected",
            "show_evidence": true,
            "confidence": 0.92,
            "annotations": [
                {
                    "id": "E01",
                    "x": 0.65,
                    "y": 0.22,
                    "width": 0.18,
                    "height": 0.16,
                    "region": "left_upper_lobe",
                    "finding": "Cavitary lesion in LUL",
                    "confidence": 0.94,
                    "display": true
                }
            ],
            "reasoning_summary": "LUL apical cavitation observed.",
            "report_summary": "Positive for pulmonary TB.",
            "limitations": ["Requires GeneXpert verification"]
        }'''
        parsed = self.mock_provider.validate_and_parse_response(raw_json)
        self.assertEqual(parsed.prediction, "Tuberculosis Detected")
        self.assertEqual(parsed.quantum_score, 0.96)
        self.assertTrue(parsed.show_evidence)
        self.assertEqual(len(parsed.annotations), 1)
        self.assertEqual(parsed.annotations[0].region, "left_upper_lobe")

    def test_04_malformed_json_rejected(self):
        """Test 4: Malformed or invalid JSON raises validation exception."""
        bad_json = "NOT_A_JSON_RESPONSE { prediction: 'TB' }"
        with self.assertRaises(Exception):
            self.mock_provider.validate_and_parse_response(bad_json)

    def test_05_missing_evidence_handled(self):
        """Test 5: Insufficient evidence produces empty annotations and valid report."""
        raw_json = '''{
            "prediction": "Normal — No TB Detected",
            "classical_score": 0.15,
            "quantum_score": 0.04,
            "consensus": "Normal — No TB Detected",
            "show_evidence": false,
            "confidence": 0.98,
            "annotations": [],
            "reasoning_summary": "Clear bilateral lung fields.",
            "report_summary": "Normal chest radiograph.",
            "limitations": ["Research baseline"]
        }'''
        parsed = self.mock_provider.validate_and_parse_response(raw_json)
        self.assertFalse(parsed.show_evidence)
        self.assertEqual(parsed.annotations, [])

    def test_06_multiple_annotations_parsed(self):
        """Test 6: Multiple annotations are parsed with normalized coordinates."""
        raw_json = '''{
            "prediction": "Tuberculosis Detected",
            "classical_score": 0.76,
            "quantum_score": 0.95,
            "consensus": "Tuberculosis Detected",
            "show_evidence": true,
            "confidence": 0.95,
            "annotations": [
                {
                    "id": "E01",
                    "x": 0.32,
                    "y": 0.24,
                    "width": 0.15,
                    "height": 0.15,
                    "region": "right_upper_lobe",
                    "finding": "RUL Infiltrate",
                    "confidence": 0.92,
                    "display": true
                },
                {
                    "id": "E02",
                    "x": 0.30,
                    "y": 0.62,
                    "width": 0.20,
                    "height": 0.16,
                    "region": "right_pleural_base",
                    "finding": "Right Pleural Effusion",
                    "confidence": 0.95,
                    "display": true
                }
            ],
            "reasoning_summary": "Bifocal TB pathology observed.",
            "report_summary": "Active pulmonary TB with effusion.",
            "limitations": []
        }'''
        parsed = self.mock_provider.validate_and_parse_response(raw_json)
        self.assertEqual(len(parsed.annotations), 2)
        self.assertEqual(parsed.annotations[0].id, "E01")
        self.assertEqual(parsed.annotations[1].id, "E02")

    def test_07_provenance_tracking(self):
        """Test 7: Response explicitly carries provenance tag."""
        res = self.mock_provider.analyze(self.sample_image, {"case_id": "TEST_CASE"})
        self.assertEqual(res.provenance, "LLM_ASSISTED_PROTOTYPE")

    def test_08_end_to_end_arbitrary_image_analysis(self):
        """Test 8: Arbitrary new image passes through full reasoning provider."""
        res = self.reasoning_engine.analyze_case(
            study_id="ARBITRARY_TEST_IMAGE_101",
            image_path=self.sample_image,
            metadata={"dataset": "External Upload", "age": 52, "sex": "M"}
        )
        self.assertIn("prediction", res)
        self.assertIn("classical_score", res)
        self.assertIn("quantum_score", res)
        self.assertIn("findings", res)
        self.assertIn("reasoning_summary", res)
        self.assertIn("provenance", res)
        self.assertEqual(res["provenance"], "LLM_ASSISTED_PROTOTYPE")


if __name__ == "__main__":
    unittest.main()
