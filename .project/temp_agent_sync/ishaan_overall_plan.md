# Ishaan (E1 & E4) - Overall Master Plan (Phases 2-4)

This document outlines all responsibilities for Ishaan across the remaining phases of the SIH26139 Hybrid Quantum AI project.

## Your Roles
- **E1 (ML/Quantum Lead):** You are responsible for all machine learning mathematics, dimensionality reduction (PCA), and Qiskit quantum kernel matrix generation.
- **E4 (Integration/DevOps Lead):** You are responsible for the CI/CD guardrails, data-leakage prevention, Pytest validation hooks, and ensuring the final backend can handle E2E API requests.

---

## Phase 2: ML Pipeline & Quantum Validation
**Objective:** Build the PyTorch-to-Qiskit bridge and prove it works without crashing.

### E1 (ML/Quantum) Tasks
- Build `src/ml/qsvm.py`.
- Write the PCA logic to reduce the 1024-dimensional DenseNet features down to strictly **8 dimensions**.
- Construct the Qiskit `ZZFeatureMap` (8 qubits, 2 repetitions).
- Generate the Quantum Kernel Matrix using `FidelityQuantumKernel` and the `AerSimulator`.
- Train the QSVM and **save the weights (`.pkl`) to disk** (this ensures the API is fast locally and scales perfectly when deployed to the cloud).

### E4 (Integration/DevOps) Tasks
- Write CI validation: `tests/phase2_tensor_shapes.py` to assert PCA outputs `(N, 8)`.
- Write CI validation: `tests/phase2_qiskit_sanity.py` to assert the Qiskit backend targets the `AerSimulator` and not a memory-heavy fallback.

---

## Phase 3: API Integration & Live Data
**Objective:** Hook the Quantum ML models into the FastAPI backend so Dharmit's frontend can consume live data.

### E1 (ML/Quantum) Tasks
- Optimize inference speed. Ensure a single X-ray can be processed through the PyTorch -> PCA -> Qiskit pipeline in under 10 seconds.
- Expose the exact `qubits`, `circuit_depth`, and `execution_stage` metrics back to the FastAPI layer so they can be sent to Dharmit's `QuantumCircuitView.tsx`.
- Build the fallback mechanism: If Qiskit crashes, the system must gracefully fall back to Classical SVM (`execution_stage: FALLBACK_CLASSICAL`).

### E4 (Integration/DevOps) Tasks
- Configure CORS in `main.py` so the Next.js frontend doesn't get blocked.
- Write E2E API tests:
  - Assert that an invalid upload (e.g., a PDF) returns `422 Unprocessable Entity` or `413 Payload Too Large`.
  - Assert that two radiologists accepting the same study simultaneously triggers a `409 Conflict`.
  - Benchmark the `/predict` route to guarantee responses under 30 seconds to prevent Vercel/Next.js timeouts.

---

## Phase 4: Final Polish & Demo Storytelling
**Objective:** Make the repository bulletproof for judges and open-source contributors.

### E1 (ML/Quantum) Tasks
- Finalize the model weights and accuracy metrics. (Remember: We are **not** claiming quantum supremacy. We are demonstrating a hybrid proof-of-concept for anomaly detection).
- Ensure the Jupiter notebooks (if any) are cleanly runnable so judges can see the math step-by-step.

### E4 (Integration/DevOps) Tasks
- Clean up all unused branches, `.pyc` files, and `node_modules` references.
- Verify `README.md` instructions work cleanly for a completely new developer.
- Run the final automated smoke tests.
