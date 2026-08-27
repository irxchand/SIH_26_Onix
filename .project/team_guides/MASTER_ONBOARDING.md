# MASTER ONBOARDING & ARCHITECTURE GUIDE

Welcome to the SIH26139 Project: **Anatomy-Grounded Hybrid Quantum AI for Early Disease Detection**. 

This document is the absolute source of truth for the entire vision, architecture, phase connections, and operational methodology of our 4-person AI-Native team. Read this carefully to understand what we are building and how we are building it.

---
## 1. What is this project? (The Core Vision)
We are building a **Hybrid Quantum-Classical Diagnostic System**. Modern healthcare relies on classical Deep Learning (like Convolutional Neural Networks) for analyzing medical images, but classical networks plateau in highly complex, highly correlated datasets. 

Our system solves this by bridging the classical and quantum worlds:
1. **Classical Vision:** We use a PyTorch U-Net to mask out anatomical noise (bones/shoulders) from Chest X-Rays, leaving only lung tissue. We then run this through a DenseNet121 to extract 1024 deep semantic features.
2. **Quantum Supremacy:** We use Principal Component Analysis (PCA) to project these 1024 features down to 8 dimensions, which are then encoded into a quantum state using a `ZZFeatureMap`. A Quantum Support Vector Machine (QSVM) evaluates the quantum kernel fidelity to detect anomalies.

By comparing the Classical SVM with the Quantum SVM on a beautiful frontend dashboard, we visually prove the advantage of Quantum Machine Learning (QML) in healthcare.

---
## 2. Our Long-Term Vision & SIH Plan
This is not just a hackathon project. This is a research endeavor. Our roadmap is defined as follows:

- **SIH Phase 1 (The Hackathon Prototype):** We execute the engineering pipeline defined in this repository. We build a flawless, decoupled architecture that proves the concept works visually and mathematically.
- **SIH Phase 2 (The Academic Publication):** Before the Grand Finale, we will compile our Classical vs Quantum fidelity metrics into an academic research paper. This validates our prototype and gives us a massive edge with the judges.
- **SIH Phase 3 (The Grand Finale):** We pitch the platform live on stage. Thanks to our DevOps Lead (E4), our system features a `dry_run` presentation mode and pre-computed quantum kernels. Even if the laptop thermal-throttles or internet drops, the API is uncrashable and the presentation will be flawless.

---
## 3. The Repository Structure
When you open the GitHub, you will see a strict organizational structure. **Do not deviate from this.**

- `docs/` -> Source of truth for product requirements, architecture decisions, and JSON interface contracts.
- `.project/` -> Team management, CI/CD planning, and these exact team guides.
- `src/` -> The actual source code.
  - `src/ml/` -> E1's domain. Scikit-Learn, Qiskit, and mathematical constraints.
  - `src/data/` -> E2's domain. PyTorch U-Net, DenseNet, and dataset splitting.
  - `src/backend/` -> E2 and E4's domain. The FastAPI routing and Pydantic schemas.
  - `frontend/` (To be created) -> E3's domain. The Next.js React application.
- `tests/` -> E4's domain. Pytest scripts to catch data leakage, routing errors, and Qiskit C++ binding failures.
- `models/` -> Where E1 saves the serialized `.joblib` models and `.npy` pre-computed quantum matrices.
- `data/` -> Where E2 places the `raw/`, `train/`, and `test/` image datasets.

---
## 4. The Global Architecture
Our system is a strictly decoupled, 3-tier architecture to ensure quantum ML logic never bottlenecks the UI.
1. **The Client (Next.js):** A premium, stateless React frontend running in the browser. It never does ML computation. It purely uploads files and visualizes JSON metrics.
2. **The API Gateway & Pipeline (FastAPI):** A Python web server. It intercepts the HTTP request, standardizes the image, masks the lungs (PyTorch U-Net), and extracts deep features (PyTorch DenseNet121).
3. **The ML Core (Scikit-Learn & Qiskit):** Classical (RBF-SVM) and Quantum (QSVM) classifiers that sit in the FastAPI memory (`app.state`), instantly predicting on the extracted features.

---
## 5. Phase Execution & Team Interlock
We operate in 3 strict engineering phases. **No one moves to the next phase until E4's automated tests pass.**

### Phase 1: Foundation & Data Preparation
- **E2 (Backend):** Downloads medical datasets, builds the PyTorch U-Net segmentation pipeline, and strictly splits data into Train/Test folders.
- **E1 (ML):** Defines the rigid mathematical tensor shape rules (e.g., PCA must yield 1x8 arrays).
- **E3 (Frontend):** Builds the entire visual shell using Next.js and hardcoded Mock JSON.
- **E4 (DevOps):** Locks down the Python virtual environment and defines the Pydantic JSON schemas. Writes anti-leakage CI tests.

### Phase 2: ML Pipeline & Core API Scaffold
- **E2 (Backend):** Runs the DenseNet feature extractor over the lungs, saving `.npy` tensors to disk. Scaffolds the FastAPI server.
- **E1 (ML):** Takes E2's `.npy` tensors and trains the PCA, SVM, and QSVM models. Computes the heavy quantum kernel matrix and saves everything as `.joblib`.
- **E3 (Frontend):** Builds the dynamic Recharts UI, linking components to React state variables.
- **E4 (DevOps):** Writes automated sanity scripts (testing Qiskit natively and dummy routing in FastAPI).

### Phase 3: Integration & Production Polish
- **E1 (ML):** Wraps the models in an `inference.py` class.
- **E2 (Backend):** Mounts E1's class into FastAPI and opens the `POST /predict` route.
- **E3 (Frontend):** Swaps in a native `fetch()` call to hit E2's API.
- **E4 (DevOps):** Configures CORS, implements the `?dry_run=true` API fallback, and does final E2E testing.

---
## 6. Zip File Initialization (DO THIS FIRST)
When you extract this project ZIP file, open it in your IDE (Antigravity/Claude). Navigate to `.project/team_guides/` and open your specific role's folder (e.g., `E1_Quantum_ML_Lead/`). 

You have two files assigned to your specific role:
1. `YOUR_ROLE_HUMAN_GUIDE.md`: **Read this yourself.** It tells you what to validate and gives you initialization prompts.
2. `YOUR_ROLE_AGENT_PROMPT.md`: **Do not read this, feed it to your agent.** 

Open your AI Agent chat and paste the prompt found in your `HUMAN_GUIDE` to inject the massive `AGENT_PROMPT` file directly into your agent's context window.
