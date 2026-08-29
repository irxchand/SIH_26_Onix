# Phase 3 - Dharmit Execution Plan

## Objective
The goal for Phase 3 is **Interactive Workstation Tools**. We need to wire up all 14 interactive UI components in the `ANATOMY // INTELLIGENCE` workstation and build the corresponding REST APIs to persist user interactions.

## Context from Phase 2
Phase 2 successfully integrated Ishaan's QSVM pipeline with the live FastAPI backend. The Next.js frontend is now properly fetching real pipeline execution metrics (qubits, circuit_depth) and rendering them in `RightIntelligence.tsx`. Live sci-fi X-Rays have been added to the `data/uploads/` directory.

## Your Tasks (E2 & E3)

### 1. Backend REST Endpoints (FastAPI)
You need to create the endpoints defined in the UI technical debt spec to support the interactive canvas tools.
Implement the following routes in `src/backend/main.py` or a dedicated router:
- `POST /api/v1/studies/{id}/calibrate`: Handles brightness, contrast, and windowing values from the Left Tool Rail.
- `POST & GET /api/v1/studies/{id}/measurements`: Persists CTR (Cardiothoracic Ratio) calipers. Implement backend validation to reject requests if there are less than 6 coordinate points!
- `POST & GET /api/v1/studies/{id}/evidence`: Saves anomaly pins and textual notes made by the radiologist.
- `POST, GET, DELETE /api/v1/studies/{id}/annotations`: Persists freehand SVG drawing paths.
- `POST /api/v1/studies/{id}/status`: Handles the final Accept/Reject classification of the study.

### 2. Frontend Interactivity (Next.js)
Wire the existing UI tools to your new backend endpoints.
- **Image Controls:** Wire the Left Tool Rail sliders (Bright, Contrast, Sharp) to dispatch to the `/calibrate` endpoint.
- **Measurements:** Wire the CTR Caliper tool. Instead of using a fake multiplier (`* 4.2`), it should use actual DICOM pixel spacing data from the backend.
- **Evidence Pins:** Make the anomaly pins interactive so the user can drag/drop them and save textual notes. POST this to the `/evidence` endpoint.
- **Freehand Drawing:** Build the SVG `<polyline>` drawing logic in `XrayCanvas.tsx` and wire it to the `/annotations` endpoint.
- **Concurrency:** Ensure the UI gracefully handles `409 Conflict` errors if multiple users try to annotate the same study simultaneously.

## Rules & Hand-off
- Strictly adhere to `schemas.py` for all Pydantic models.
- When you are finished, ensure you run `pytest tests/phase3_endpoint_validation.py` (which I will create soon) to validate your endpoints.
- Push your work to `phase_1` and prompt Ishaan to proceed with Phase 3 ML integration.
