# Phase 3 - Ishaan Execution Plan

## Objective
The goal for Phase 3 is **Interactive Workstation Tools**. While Dharmit wires the UI interactivity, I will transition the backend from using mocked sleep timers to loading actual PyTorch models for inference, and enforcing data validation on the interactivity endpoints.

## Your Tasks (E1)

### 1. PyTorch Integration
- Ensure `feature_extraction.py` correctly loads the DenseNet121 model.
- Load the PyTorch models (U-Net and DenseNet121) during the FastAPI `@app.lifespan` hook so they are kept in memory and don't slow down inference.
- Replace the `asyncio.sleep` blocks in the ML pipeline with actual synchronous PyTorch execution (run in threadpools if necessary).

### 2. Validation Logic
- Work with Dharmit to ensure the `schemas.py` models for the new interactive endpoints are mathematically robust.
- Add backend verification for CTR measurements to ensure biological plausibility (e.g., rejecting invalid bounding box coordinates).
- Write `tests/phase3_endpoint_validation.py` to test Dharmit's newly created endpoints (`/calibrate`, `/measurements`, `/annotations`, `/evidence`, `/status`).

### 3. QSVM Handoff Optimization
- Ensure that the PyTorch tensors are correctly flattened and scaled before being passed into the 8-dimensional PCA feature map of the QSVM.

## Next Steps
- Wait for Dharmit to build the basic endpoints and UI.
- Once Dharmit finishes his Phase 3 integration, execute this plan to tie the real ML logic to his endpoints.
