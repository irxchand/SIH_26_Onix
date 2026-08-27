# Requirements

## Confirmed MVP Requirements (Internal PoW)
- **Input:** Ingest a standard Chest X-Ray (CXR) image via REST API.
- **Backend (FastAPI):**
  - Standardize image and perform lung segmentation.
  - Extract deep features using DenseNet121.
  - Apply PCA to reduce features (4-8 dims).
  - Run inference with RBF-SVM and Qiskit QSVM.
- **Frontend (Next.js):**
  - Premium, responsive UI (Tailwind, Framer Motion).
  - Consume FastAPI REST endpoints (multipart/form-data).
- **Output:** Basic visual explanation (Grad-CAM) and comparative benchmark metrics.
- **Safety:** Clear non-clinical research disclaimer.

## System Boundaries
- Frontend is strictly UI-focused, no ML processing.
- Backend is stateless and capable of local execution for PoW, Docker deployment for Phase 4.
