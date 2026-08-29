# Phase 2 Implementation Plan (Ishaan: E1 & E4)

As per the Master Execution Plan, Phase 2 moves us from static scaffolding to **Live ML Pipelines and Core APIs**. For your roles (E1 and E4), this involves mathematically enforcing the quantum constraints while actually building the PyTorch-to-Qiskit inference pipeline.

## User Review Required
> [!IMPORTANT]
> Since training a full SVM and generating a Quantum Kernel Matrix locally can easily cause an Out of Memory (OOM) error or freeze your system, this plan relies heavily on Qiskit's `AerSimulator` and caps qubits at 8. **Do you approve capping the test dataset strictly to 100 samples for the local training loop to ensure it doesn't crash during development?**

## Open Questions
> [!WARNING]
> Do you want the trained PCA and QSVM model weights saved to disk (e.g., `src/ml/weights/pca.pkl`) during the training script so the FastAPI backend can load them instantaneously during inference? Or do you want the server to retrain dynamically on startup (not recommended)?

## Proposed Changes

---

### Machine Learning & Quantum Pipeline (E1)
This component builds the mathematical bridge between the classical features and the quantum simulator.

#### [NEW] [src/ml/qsvm.py](file:///d:/Users/Documents/Symbiosis/Hackathons/SIH%2026/src/ml/qsvm.py)
- Implement `train_pca()`: Reduces the 1024-dimensional PyTorch embeddings down to exactly 8 dimensions (using `constants.PCA_COMPONENTS`).
- Implement `construct_quantum_kernel()`: Builds a `ZZFeatureMap` with 8 qubits and 2 repetitions, using Qiskit's `FidelityQuantumKernel` backed by `AerSimulator`.
- Implement `train_qsvm()`: Fits a classical `SVC(kernel="precomputed")` using the quantum kernel matrix.

### Automated Validation Hooks (E4)
These test scripts will run automatically in CI to enforce the project constraints before Dharmit merges his Phase 2 work.

#### [NEW] [tests/phase2_tensor_shapes.py](file:///d:/Users/Documents/Symbiosis/Hackathons/SIH%2026/tests/phase2_tensor_shapes.py)
- Asserts that the PyTorch output matches `(N, 1024)` before PCA.
- Asserts that PCA output matches `(N, 8)`.

#### [NEW] [tests/phase2_qiskit_sanity.py](file:///d:/Users/Documents/Symbiosis/Hackathons/SIH%2026/tests/phase2_qiskit_sanity.py)
- Instantiates the `ZZFeatureMap` and programmatically asserts `feature_map.num_qubits == 8`.
- Verifies that the Qiskit backend is correctly targeting `aer_simulator` and not a generic statevector fallback that would cause OOM.

#### [NEW] [tests/phase2_endpoint_validation.py](file:///d:/Users/Documents/Symbiosis/Hackathons/SIH%2026/tests/phase2_endpoint_validation.py)
- A placeholder test file ready to validate Dharmit's `/queue` and `/upload` endpoints once he pushes them.

## Verification Plan

### Automated Tests
- `pytest tests/phase2_tensor_shapes.py`
- `pytest tests/phase2_qiskit_sanity.py`

### Manual Verification
- Execute `python src/ml/qsvm.py` locally to ensure the QSVM trains without crashing or freezing the workstation.
- We will commit this plan as a markdown file inside `.project/planning_steps/` so Dharmit can reference exactly what the ML pipeline requires of his data loader.
