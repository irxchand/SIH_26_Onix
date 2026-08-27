# Implementation Plan

## Phase 1: API & Data Foundation
- Scaffold FastAPI backend.
- Implement PyTorch inference for Lung Segmentation + DenseNet121.
- Fit PCA on the training set.

## Phase 2: QML & Classical Baselines
- Train Classical RBF-SVM on PCA features.
- Build Qiskit `ZZFeatureMap` + `FidelityQuantumKernel`.
- Save QSVC model and pre-computed kernel matrix.

## Phase 3: Modern Frontend
- Scaffold Next.js application.
- Build premium UI components (Upload, Dashboard, Comparison Cards).
- Connect to FastAPI endpoints and implement smooth loading states.

## Phase 4: Smoke Testing
- Implement dummy data pipelines.
- Verify Qiskit circuit sanity tests.
- Finalize `dry_run` fallback functionality.
