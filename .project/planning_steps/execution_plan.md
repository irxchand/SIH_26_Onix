# Execution & Resource Allocation Plan

## 1. Team Composition & Personas
To ensure cross-functional contribution across all 4 engineers while maintaining expert focus:
- **E1 (ML/Quantum Lead):** Focuses on Qiskit, PCA, SVM, and model saving/loading.
- **E2 (Backend/Data Engineer):** Focuses on PyTorch (UNet/DenseNet), FastAPI routing, and data pipelines.
- **E3 (Frontend Engineer):** Focuses on Next.js, Tailwind, visualizations, and UI state.
- **E4 (Integration/DevOps Lead):** Focuses on testing, CORS, E2E integrations, and building the automated validation hooks for your validating agent.

---

## 2. Execution Phases & Time Estimates (Based on 3-Day Sprint)

### Phase 1: Foundation & Data Pipeline (Estimated Time: 6-8 Hours)
**Goal:** Environments exist, data is preprocessed, UI is mocked.
- **E1 (20%):** Define mathematical shape constraints for PCA/Tensors.
- **E2 (40%):** Write `download_datasets.py` and `segmentation.py`.
- **E3 (30%):** Scaffold Next.js and build a mocked static dashboard.
- **E4 (10%):** Setup `uv` virtual env, scaffold FastAPI, and define strict Pydantic JSON schemas.

**RISK VALIDATION (Where things go wrong here):**
- *Risk:* Data Leakage. If E2 normalizes or fits scalars on the whole dataset before splitting, the entire benchmark is invalid.
- *Agent Validator Hook Check:* Your agent will run a script checking that `StandardScaler` is explicitly fit *after* `train_test_split`.

### Phase 2: ML Pipeline & Core API (Estimated Time: 8-10 Hours)
**Goal:** Models are trained, API can serve predictions, core data endpoints are live.
- **E1 (50%):** Train PCA, RBF-SVM, construct `ZZFeatureMap`, and pre-compute the Quantum Kernel Matrix.
- **E2 (30%):** Write `feature_extraction.py` (DenseNet), load models into FastAPI `@app.lifespan`, and build the following endpoints (see `ui_technical_debt.md` for full specs):
  - `GET /api/v1/queue` — paginated study list with search/status filters.
  - `POST /api/v1/upload` — multipart image upload, file type validation (JPEG/PNG/DICOM, max 50MB).
  - `GET /api/v1/studies/{id}/metadata` — return DICOM pixel spacing, dimensions, tags.
  - `GET /api/v1/studies/{id}/segmentation` — return normalized SVG path strings from U-Net inference.
  - Expand `POST /api/v1/predict` payload to include `{ qubits, circuit_depth, feature_map, simulator, execution_stage, evidence[] }`.
- **E3 (10%):** Replace `mockStudies` with live `fetch` to `/api/v1/queue`. Implement live image upload with progress bar. Replace hardcoded SVG lung paths with data from `/segmentation`.
- **E4 (10%):** Write dummy tensor tests `test_dummy_pipeline.py`.

🔴 **RISK VALIDATION (Where things go wrong here):**
- *Risk:* Memory Overflow / Hanging. Computing a $500 \times 500$ quantum kernel matrix locally might hang or OOM (Out of Memory).
- *Agent Validator Hook Check:* Your agent will verify the quantum script strictly uses `AerSimulator` and that the matrix calculation is batched or limits qubits $\le 8$.

### Phase 3: Integration & Final Polish (Estimated Time: 8 Hours)
**Goal:** E2E system works flawlessly. Every UI tool hits a real endpoint.
- **E1 (10%):** Extract confidence scores, track true quantum metrics (depth/qubits), return them via prediction payload. Handle simulator fallback (`execution_stage: FALLBACK_CLASSICAL`).
- **E2 (35%):** Build the remaining 9 endpoints (see `ui_technical_debt.md` Summary Table):
  - `POST /api/v1/studies/{id}/measurements` — save CTR points, ratio, notes. Validate ≥6 points, reject div-by-zero.
  - `GET /api/v1/studies/{id}/measurements` — retrieve saved measurements.
  - `POST /api/v1/studies/{id}/evidence/{evidenceId}/notes` — save observation notes on anomaly pins.
  - `GET /api/v1/studies/{id}/evidence` — full evidence array with saved notes.
  - `POST /api/v1/studies/{id}/status` — accept/reject with `409 Conflict` for race conditions.
  - `POST /api/v1/studies/{id}/calibrate` — backend DICOM windowing/calibration.
  - `POST /api/v1/studies/{id}/annotations` — save freehand polylines and text markers.
  - `GET /api/v1/studies/{id}/annotations` — retrieve all annotations.
  - `DELETE /api/v1/studies/{id}/annotations/{annotationId}` — delete individual annotations.
- **E3 (35%):** Wire every UI tool to its corresponding endpoint:
  - **MEASURE**: Replace `* 4.2` multiplier with real pixel spacing from `/metadata`. Block Save on < 6 points. Handle div-by-zero gracefully.
  - **EVIDENCE**: Load pins from `/predict` payload. Wire note saving to `/evidence/{id}/notes`.
  - **ACCEPT/REJECT**: Wire to `/status`. Handle `409` race condition with modal. Transition to Queue on success.
  - **SCAN**: Implement frontend pan/zoom (click-drag + scroll). Wire backend calibration to `/calibrate` with fallback.
  - **ANNOTATE**: Implement freehand SVG `<polyline>` drawing + text markers. Downsample strokes to ≤200 points. Wire to `/annotations`.
  - **PIPELINE**: Replace `setTimeout` animation with polling `/api/v1/predict` status. Add timeout + retry.
  - **QUANTUM METRICS**: Replace hardcoded `92.4%`/`91.8%`/`Qubits: 8`/`Depth: 24` with live payload data. Handle `NaN` confidence.
- **E4 (20%):** Configure CORS, implement `?dry_run=true` fallback, and run final E2E smoke tests:
  - Test incomplete measurement submissions (expect `422`).
  - Test race condition on accept/reject (expect `409`).
  - Test oversized file upload (expect `413`).
  - Test QSVM timeout handling (assert response < 30s or fallback).

🔴 **RISK VALIDATION (Where things go wrong here):**
- *Risk:* HTTP Timeout. QSVM inference takes too long (e.g., >30s) causing the Next.js fetch to timeout.
- *Agent Validator Hook Check:* Your agent will trigger the API and assert response time. If $>10s$, it flags E4 to increase timeout limits or optimize the inference loop.
- *Risk:* Race conditions on `/status`. Two radiologists accept simultaneously.
- *Agent Validator Hook Check:* E4 writes a concurrent request test hitting `/status` twice in parallel and asserts exactly one `200` and one `409`.

---

## 3. Automated Validation Strategy (For your Validating Agent)
Once execution begins, your agent will act as a strict CI/CD gatekeeper. At the end of each Phase, it will run specific scripts located in `tests/`:
1. `pytest tests/phase1_data_leakage.py`
2. `pytest tests/phase2_tensor_shapes.py`
3. `pytest tests/phase2_qiskit_sanity.py`
4. `pytest tests/phase2_endpoint_queue_upload.py` — validates `/queue` and `/upload` return correct schemas.
5. `pytest tests/phase3_e2e_api.py`
6. `pytest tests/phase3_measurements.py` — validates measurement save/retrieve, 422 on incomplete data.
7. `pytest tests/phase3_annotations.py` — validates annotation CRUD, polyline downsampling.
8. `pytest tests/phase3_race_conditions.py` — validates concurrent `/status` calls return 200 + 409.

*Only when the agent outputs all green checks will the team proceed to the next phase.*
