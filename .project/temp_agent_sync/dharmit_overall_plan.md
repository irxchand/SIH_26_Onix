# Dharmit (E2 & E3) - Overall Master Plan (Phases 2-4)

This document outlines all responsibilities for Dharmit across the remaining phases of the SIH26139 Hybrid Quantum AI project.

## Your Roles
- **E2 (Backend/Data Engineer):** You are responsible for PyTorch data ingestion, U-Net segmentation, FastAPI routing, and building all the endpoints specified in `ui_technical_debt.md`.
- **E3 (Frontend Engineer):** You are responsible for the Next.js `ANATOMY // INTELLIGENCE` workstation, managing complex React state, and wiring the UI to your own backend endpoints.

---

## Phase 2: Core Endpoints & Live Connections
**Objective:** Replace hardcoded mocks with live API calls.

### E2 (Backend/Data) Tasks
- Implement real dataset downloads in `download_datasets.py` (Shenzhen & Montgomery).
- Implement PyTorch DenseNet121 extraction in `feature_extraction.py`.
- Build the Phase 2 API endpoints:
  - `GET /api/v1/queue`
  - `POST /api/v1/upload`
  - `GET /api/v1/studies/{id}/metadata`
  - `GET /api/v1/studies/{id}/segmentation`
- Load the pre-trained ML weights (saved by Ishaan) into FastAPI using the `@app.lifespan` context manager so they are kept in memory.

### E3 (Frontend) Tasks
- Wire the `RadiologyQueue` to fetch from `GET /api/v1/queue` instead of using `mockStudies`.
- Wire the Custom Scan Importer to `POST /api/v1/upload` and show a loading bar.
- Update `XrayCanvas.tsx` to render the SVG lung paths fetched from the backend segmentation endpoint instead of the hardcoded paths.

---

## Phase 3: Interactive Workstation Tools
**Objective:** Wire up all 14 interactive components in the workstation.

### E2 (Backend/Data) Tasks
- Build the remaining 9 API endpoints required by `ui_technical_debt.md`:
  - `POST & GET /api/v1/studies/{id}/measurements` (CTR calculations)
  - `POST & GET /api/v1/studies/{id}/evidence...` (Anomaly Pins)
  - `POST /api/v1/studies/{id}/status` (Accept/Reject)
  - `POST /api/v1/studies/{id}/calibrate` (Pan/Zoom/Windowing)
  - `POST, GET, DELETE /api/v1/studies/{id}/annotations` (Freehand drawing)
- Strictly enforce backend validation (e.g., rejecting CTR measurements if there are < 6 points).

### E3 (Frontend) Tasks
- Wire the Left Tool Rail (Brightness/Contrast/Sharpness/Zoom) to the backend `/calibrate` endpoint.
- Wire the CTR Caliper tool so it replaces the fake `* 4.2` multiplier with actual DICOM pixel spacing from the backend.
- Make the Evidence pins interactive and save notes to the backend.
- Build the freehand drawing SVG `<polyline>` logic and wire it to the `/annotations` endpoints.
- Manage React state so that if multiple radiologists are working, the UI handles `409 Conflict` gracefully.

---

## Phase 4: Final Polish & Demo Storytelling
**Objective:** Ensure the visual and functional experience blows the judges away.

### E2 (Backend/Data) Tasks
- Optimize PyTorch inference logic to ensure it doesn't bottleneck Ishaan's QSVM execution.
- Ensure all endpoints have clean error handling (`HTTPException`) so the frontend doesn't crash on bad JSON.

### E3 (Frontend) Tasks
- Add micro-animations (e.g., skeleton loaders, transition fades) when the Quantum Pipeline is executing.
- Ensure the UI looks impeccable on a 1080p projector (the standard Hackathon presentation format).
- Write frontend error boundaries so that if a single API call fails, the entire workstation doesn't white-screen.
