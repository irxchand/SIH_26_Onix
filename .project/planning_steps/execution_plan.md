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
**Goal:** Models are trained, API can serve predictions.
- **E1 (50%):** Train PCA, RBF-SVM, construct `ZZFeatureMap`, and pre-compute the Quantum Kernel Matrix.
- **E2 (30%):** Write `feature_extraction.py` (DenseNet) and load models into FastAPI `@app.lifespan`.
- **E3 (10%):** Build dynamic charts (Chart.js / Recharts) ready to accept JSON.
- **E4 (10%):** Write dummy tensor tests `test_dummy_pipeline.py`.

🔴 **RISK VALIDATION (Where things go wrong here):**
- *Risk:* Memory Overflow / Hanging. Computing a $500 \times 500$ quantum kernel matrix locally might hang or OOM (Out of Memory).
- *Agent Validator Hook Check:* Your agent will verify the quantum script strictly uses `AerSimulator` and that the matrix calculation is batched or limits qubits $\le 8$.

### Phase 3: Integration & Final Polish (Estimated Time: 6 Hours)
**Goal:** E2E system works flawlessly.
- **E1 (10%):** Extract confidence scores and write UI tooltips explaining the quantum advantage (if any).
- **E2 (30%):** Finalize the `/api/v1/predict` endpoint, ensuring file uploads stream correctly into PyTorch.
- **E3 (40%):** Swap mock data for real API `fetch` calls, handle `isPending` loading states.
- **E4 (20%):** Configure CORS, implement the `?dry_run=true` fallback, and run final E2E smoke tests.

🔴 **RISK VALIDATION (Where things go wrong here):**
- *Risk:* HTTP Timeout. QSVM inference takes too long (e.g., >30s) causing the Next.js fetch to timeout.
- *Agent Validator Hook Check:* Your agent will trigger the API and assert response time. If $>10s$, it flags E4 to increase timeout limits or optimize the inference loop.

---

## 3. Automated Validation Strategy (For your Validating Agent)
Once execution begins, your agent will act as a strict CI/CD gatekeeper. At the end of each Phase, it will run specific scripts located in `tests/`:
1. `pytest tests/phase1_data_leakage.py`
2. `pytest tests/phase2_tensor_shapes.py`
3. `pytest tests/phase2_qiskit_sanity.py`
4. `pytest tests/phase3_e2e_api.py`

*Only when the agent outputs all green checks will the team proceed to the next phase.*
