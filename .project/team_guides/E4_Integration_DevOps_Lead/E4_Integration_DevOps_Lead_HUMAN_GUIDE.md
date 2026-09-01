# 🧑‍💻 E4 - Integration & DevOps Lead (Deep Execution & Validation Guide)

## 1. Core Philosophy & Role Definition
As the Integration and DevOps Lead, you are the final gatekeeper of the project. If the code breaks during the hackathon presentation, it is your responsibility. Your job is to define strict API contracts so E2 and E3 can work in parallel without breaking each other, build automated tests to ensure E1 doesn't leak data, and build the ultimate presentation fallback mode (`dry_run`).

**The inherent problem you are solving:** Hackathon projects look great on laptops but crash on the projector. Quantum simulators are highly sensitive to thermal throttling and OS-level C++ binding errors. You must write scripts that prove the quantum environment is functional before the pitch, and you must build an API escape hatch to bypass the ML entirely if things go wrong live on stage.

Your AI Agent is great at writing `pytest` scripts, but you must ensure it tests the *actual mathematical boundaries* rather than just checking if a function returns `True`.

---

## 2. Phase 1: Scaffolding & Strict Schemas Validation

### The Objective
Lock down the Python environment and define the JSON contract that the backend will return and the frontend will parse.

### What to Manually Check & Validate
1. **The Pydantic Schema:** 
   - *Detail Check:* Open `src/backend/schemas.py`. Does it match the `PredictionResponse` structure from `docs/06_interfaces.md` exactly? Ensure fields like `classical_svm.confidence` are typed as `float` and `filename` as `str`.
2. **The Anti-Leakage Test:**
   - *Detail Check:* E1's PCA model must never see test data. Look at `tests/phase1_data_leakage.py`. The agent must use `joblib.load('models/scaler.joblib')` and check `scaler.n_samples_seen_`. It must count the physical files in `data/train/` and assert they match. If the agent wrote a test that just checks `len(X_train) == len(y_train)`, reject it. It must check the serialized `.joblib` state.

### Agent Prompts (Phase 1)
**Initialization Prompt:**
> "Agent, I am E4, the DevOps Lead. Load your system directives from `E4_Integration_DevOps_Lead_AGENT_PROMPT.md`. We are executing Phase 1. Use `uv venv` to initialize. Create `requirements.txt`. Define the `PredictionResponse` Pydantic model exactly as specified in the docs. Then write the strict `pytest` data-leakage script that verifies the scaler's `n_samples_seen_` matches the training directory count. Stop when done for my review."

**Correction Prompt (If the test is too generic):**
> "Your `phase1_data_leakage.py` test is too generic. I don't care if the numpy arrays match in memory during runtime. I need you to load the physical `models/scaler.joblib` file from disk, read its `n_samples_seen_` attribute, and assert that it equals the physical file count in `data/train/`. Rewrite it."

---

## 3. Phase 2: Smoke Testing & Sanity Checks Validation

### The Objective
Guarantee that the heavy ML frameworks do not crash the host machine during API routing.

### What to Manually Check & Validate
1. **Dummy Tensor Routing:**
   - *Detail Check:* The FastAPI server (E2) must be tested without needing the real 500MB PyTorch models. Look at `tests/test_dummy_pipeline.py`. The agent MUST mock `app.state.unet` to return a random `(1, 1, 224, 224)` tensor, and mock `app.state.ml_inference.predict` to return a fake JSON. 
   - *Validation:* Run `pytest tests/test_dummy_pipeline.py`. If it passes, E2's FastAPI `UploadFile` byte-reading logic is mathematically sound.
2. **Qiskit Native Sanity Test:**
   - *Detail Check:* Run `pytest tests/test_qiskit_sanity.py`. It should execute a simple 1-qubit Pauli-X gate on `AerSimulator`. If this fails, your C++ compiler or Python environment is broken. Re-install Qiskit immediately.

### Agent Prompts (Phase 2)
**Execution Prompt:**
> "Agent, proceed to Phase 2. We need isolated smoke tests. Write `test_dummy_pipeline.py` using `fastapi.testclient.TestClient`. Use `unittest.mock` to mock `app.state.unet` and `densenet` so they return random tensors of the correct shapes. Then write `test_qiskit_sanity.py` to ensure `AerSimulator` can execute a basic Pauli-X circuit without throwing OS-level binary errors."

---

## 4. Phase 3: CORS & Dry-Run Fallback Validation

### The Objective
Connect the frontend to the backend securely, and build the ultimate presentation fallback mode.

### What to Manually Check & Validate
1. **CORS Configuration:**
   - *Detail Check:* Inspect `src/backend/main.py`. The agent must have added `CORSMiddleware`. Ensure `allow_origins` includes `http://localhost:3000` (E3's Next.js port).
2. **The Dry-Run Escape Hatch:**
   - *Detail Check:* In `src/backend/main.py`, the `POST /predict` route must now accept `dry_run: bool = False`. 
   - *Validation:* If `dry_run=True`, the code MUST NOT call `app.state.densenet` or `app.state.ml_inference`. It must `await asyncio.sleep(1.5)` (to fake computation time) and return a hardcoded success JSON. Test this manually in Swagger UI before the pitch.

### Agent Prompts (Phase 3)
**Execution Prompt:**
> "Agent, proceed to Phase 3. Add `CORSMiddleware` to FastAPI. Then, modify the `/predict` route. Add an optional query parameter `?dry_run=false`. If true, bypass ALL PyTorch and Qiskit logic. Sleep for 1.5 seconds, and return a perfectly formatted fake `PredictionResponse`. This is our fail-safe for the live presentation. Finally, write an E2E test to validate the real endpoint."
