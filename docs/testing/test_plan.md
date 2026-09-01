# Test Plan

## Smoke Testing Strategy
- **Dummy Data Pipeline:** Inject a random 224x224 noise array into FastAPI to verify routing and JSON response structure before loading heavy PyTorch/Qiskit libraries.
- **Qiskit Sanity Test:** Run a 1-qubit `ZZFeatureMap` on `AerSimulator` to ensure the quantum environment is functional on the host machine.
- **Dry-Run API Mode:** Test the `?dry_run=true` endpoint parameter to verify fallback UI behavior during presentation scenarios.

## Methodological Verification
- Assert that PCA and Scalers are fitted exclusively on the training dataset.
- Validate quantum feature map limits (max 8 qubits) to avoid memory overflow on the presentation hardware.
