# Architecture

## Design Principles
- **Decoupled Architecture:** Next.js (Client) + FastAPI (Inference Server).
- **API-First Contract:** Strict REST JSON schema for frontend/backend communication.
- **Autonomy Boundaries:** Frontend agents decide UI aesthetics; Backend agents strictly handle pure functional ML/QML pipelines.

## Container View
1. **Next.js Client:** State management, Upload Widgets, Metrics Dashboard.
2. **FastAPI Backend:** Routing, ML/QML Pipeline, Background Tasks.

## Component View (Backend)
- **Preprocessor & Segmentation:** PyTorch / UNet.
- **Feature Encoder:** Pretrained DenseNet121.
- **Dimensionality Reduction:** Scikit-learn PCA.
- **Classical Classifier:** Scikit-learn SVC (RBF kernel).
- **Quantum Classifier:** Qiskit Machine Learning (QSVM, ZZFeatureMap, AerSimulator).

## Data Encoding
- Qiskit `ZZFeatureMap` (entangling, up to 8 qubits).
- Pre-computed kernel matrices for training data to mitigate simulation bottlenecks.
