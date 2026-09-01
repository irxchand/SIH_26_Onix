"""
Automated Test Suite for Dynamic Edge-Case Prompt Generation & Information Flow.
Tests 10 distinct edge cases verifying that prompts adapt dynamically to available information.
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.backend.prompt_builder import build_edge_case_prompt
from src.backend.evidence_collector import LocalEvidenceCollector


def run_edge_case_tests():
    collector = LocalEvidenceCollector(encoder_name="densenet121")
    sample_img = "data/datasets/montgomery/MontgomerySet/CXR_png/MCUCXR_0001_0.png"
    if not Path(sample_img).exists():
        all_pngs = list(Path("data").glob("**/*.png"))
        if all_pngs:
            sample_img = str(all_pngs[0])
        else:
            raise FileNotFoundError("No sample CXR png found for testing.")

    print("==================================================")
    print("RUNNING 10 EDGE-CASE PROMPT GENERATION TEST SUITES")
    print("==================================================")

    # Test 1: Completely unknown X-ray (No metadata, no scores, basic image metrics)
    print("\n--- TEST 1: Completely Unknown X-Ray ---")
    ev1 = collector.collect(sample_img, study_id="JUDGE_UNKNOWN_001")
    prompt1 = build_edge_case_prompt(sample_img, available_evidence=ev1)
    assert "CURRENT CASE: UNKNOWN / JUDGE-SUPPLIED CHEST X-RAY" in prompt1
    assert "ACTUAL MODEL SCORE" not in prompt1
    assert "Classical score real: False" in prompt1
    assert "Quantum score real: False" in prompt1
    print("✓ Test 1 Passed: Prompt properly flags unverified external case with no assumed labels.")

    # Test 2: Unknown X-ray + Segmentation available
    print("\n--- TEST 2: Unknown X-Ray + Segmentation ---")
    ev2 = collector.collect(sample_img, study_id="JUDGE_SEG_002")
    ev2["segmentation"] = {"leftLung": "M10,20 L30,40", "rightLung": "M60,20 L80,40"}
    ev2["segmentation_confidence"] = 0.985
    prompt2 = build_edge_case_prompt(sample_img, available_evidence=ev2)
    assert "Anatomical Segmentation: Available (U-Net / Anatomical contour) (Confidence: 0.985)" in prompt2
    print("✓ Test 2 Passed: Prompt dynamically embeds real segmentation contours & confidence.")

    # Test 3: Unknown X-ray + Actual Classical Score
    print("\n--- TEST 3: Unknown X-Ray + Actual Classical Score ---")
    ev3 = collector.collect(sample_img, study_id="JUDGE_CLASSICAL_003")
    ev3["classical_result"] = {"score": 0.742, "prediction": "Tuberculosis Detected"}
    prompt3 = build_edge_case_prompt(sample_img, available_evidence=ev3)
    assert "Classical Model Output: ACTUAL MODEL SCORE: 0.742" in prompt3
    assert "Classical score real: True" in prompt3
    assert "Quantum score real: False" in prompt3
    print("✓ Test 3 Passed: Prompt preserves genuine classical score and requests quantum estimate.")

    # Test 4: Unknown X-ray + Actual Quantum Score
    print("\n--- TEST 4: Unknown X-Ray + Actual Quantum Score ---")
    ev4 = collector.collect(sample_img, study_id="JUDGE_QUANTUM_004")
    ev4["quantum_result"] = {"score": 0.965, "prediction": "Tuberculosis Detected", "qubits": 8}
    prompt4 = build_edge_case_prompt(sample_img, available_evidence=ev4)
    assert "Quantum Model Output: ACTUAL MODEL SCORE: 0.965" in prompt4
    assert "Quantum score real: True" in prompt4
    assert "Classical score real: False" in prompt4
    print("✓ Test 4 Passed: Prompt preserves genuine quantum score and requests classical estimate.")

    # Test 5: Unknown X-ray + Both Classical and Quantum Scores
    print("\n--- TEST 5: Unknown X-Ray + Both Model Scores ---")
    ev5 = collector.collect(sample_img, study_id="JUDGE_BOTH_005")
    ev5["classical_result"] = {"score": 0.735, "prediction": "Tuberculosis Detected"}
    ev5["quantum_result"] = {"score": 0.958, "prediction": "Tuberculosis Detected"}
    prompt5 = build_edge_case_prompt(sample_img, available_evidence=ev5)
    assert "Classical Model Output: ACTUAL MODEL SCORE: 0.735" in prompt5
    assert "Quantum Model Output: ACTUAL MODEL SCORE: 0.958" in prompt5
    assert "Classical score real: True" in prompt5
    assert "Quantum score real: True" in prompt5
    print("✓ Test 5 Passed: Prompt preserves both genuine scores and focuses on reasoning & evidence.")

    # Test 6: Unknown X-ray + No Model Outputs
    print("\n--- TEST 6: Unknown X-Ray + No Model Outputs ---")
    ev6 = collector.collect(sample_img, study_id="JUDGE_BLIND_006")
    ev6["classical_result"] = None
    ev6["quantum_result"] = None
    prompt6 = build_edge_case_prompt(sample_img, available_evidence=ev6)
    assert "Classical Model Output: UNAVAILABLE" in prompt6
    assert "Quantum Model Output: UNAVAILABLE" in prompt6
    print("✓ Test 6 Passed: Prompt explicitly marks models UNAVAILABLE without inventing missing values.")

    # Test 7: Abnormal image with localized clinical history
    print("\n--- TEST 7: Abnormal Image with Localized Context ---")
    meta7 = {"clinical_indication": "Active cough, left upper lobe opacity reported", "dataset": "External Hospital"}
    ev7 = collector.collect(sample_img, study_id="JUDGE_ABNORMAL_007", metadata=meta7)
    prompt7 = build_edge_case_prompt(sample_img, available_evidence=ev7, metadata=meta7)
    assert "Active cough, left upper lobe opacity reported" in prompt7
    assert "PATIENT'S LEFT LUNG" in prompt7
    print("✓ Test 7 Passed: Prompt integrates clinical indication and references target anatomical quadrant.")

    # Test 8: Normal image
    print("\n--- TEST 8: Normal Image ---")
    meta8 = {"clinical_indication": "Routine pre-employment screening, clear lung fields"}
    ev8 = collector.collect(sample_img, study_id="JUDGE_NORMAL_008", metadata=meta8)
    prompt8 = build_edge_case_prompt(sample_img, available_evidence=ev8, metadata=meta8)
    assert "Routine pre-employment screening" in prompt8
    assert "show_evidence: false" in prompt8
    print("✓ Test 8 Passed: Prompt enforces show_evidence: false and empty annotations for normal scans.")

    # Test 9: Ambiguous Image
    print("\n--- TEST 9: Ambiguous Image ---")
    meta9 = {"clinical_indication": "Borderline costophrenic blunting vs respiratory artifact"}
    ev9 = collector.collect(sample_img, study_id="JUDGE_AMBIGUOUS_009", metadata=meta9)
    prompt9 = build_edge_case_prompt(sample_img, available_evidence=ev9, metadata=meta9)
    assert "Borderline costophrenic blunting" in prompt9
    print("✓ Test 9 Passed: Prompt guides synthesis on ambiguous visual presentation.")

    # Test 10: Poor-Quality Image
    print("\n--- TEST 10: Poor-Quality / Degraded Image ---")
    ev10 = collector.collect(sample_img, study_id="JUDGE_POOR_010")
    ev10["image_info"]["quality"] = "Low contrast / degraded exposure"
    prompt10 = build_edge_case_prompt(sample_img, available_evidence=ev10)
    assert "Visual Quality: Low contrast / degraded exposure" in prompt10
    print("✓ Test 10 Passed: Prompt explicitly alerts ChatGPT of degraded exposure.")

    print("\n==================================================")
    print("ALL 10 EDGE-CASE PROMPT GENERATION TESTS PASSED ✓")
    print("==================================================")


if __name__ == "__main__":
    run_edge_case_tests()
