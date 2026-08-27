# System Design

## 1. High-Level Design
The system is fully decoupled into two main containers:
- **Next.js Client:** Handles all UI rendering, routing, file uploads, and state management. Runs in the browser.
- **FastAPI Inference Service:** A stateless REST API backend handling heavy machine learning and quantum simulations. 

## 2. Mid-Level Design (Modules)
- **Preprocessor:** Normalizes and resizes CXR images.
- **Segmentation:** Extracts lung mask using PyTorch.
- **Feature Encoder:** Passes masked lung through DenseNet121.
- **Dimensionality Reducer:** PCA compresses 1024D vector to 8D.
- **Inference Router:** Routes 8D vector to both RBF-SVM and QSVM simultaneously.
- **Explanation Generator:** Calculates Grad-CAM heatmaps.

## 3. Low-Level Execution Guidelines
- **Frontend Agents:** Allowed full autonomy over to the human operator for the styling, colors, and layout components. Must strictly mock API responses before integration.
- **Backend Agents:** Must use functional programming. Stateful objects (PCA, SVM models) are loaded once into memory during the FastAPI lifespan hook.
