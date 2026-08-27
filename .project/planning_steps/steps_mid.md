# Mid-Level Steps (The Component View)

## 1. System & Repository Initialization
- Set up the Python virtual environment and core ML dependencies.
- Scaffold the Next.js project and Tailwind CSS configuration.

## 2. Data Engineering & Preprocessing Pipeline
- Download and normalize the CXR datasets (e.g., Montgomery/Shenzhen).
- Implement Lung Segmentation using a pretrained network (e.g., U-Net).
- Extract dense features (1024D) from the segmented lungs using a pretrained DenseNet121.
- Split the dataset strictly into training and testing sets to prevent data leakage.

## 3. Machine Learning Pipeline
- Fit a PCA dimensionality reducer exclusively on the training set to compress features from 1024D to 8D.
- Train the classical baseline classifier (RBF-SVM) on the 8D training set.
- Construct the Qiskit Quantum Feature Map (e.g., 8-qubit ZZFeatureMap).
- Pre-compute the computationally heavy quantum kernel matrix for the training set.
- Train the Quantum Support Vector Classifier (QSVC) using the pre-computed matrix.
- Serialize and save all trained models/matrices to disk.

## 4. Backend API Development
- Scaffold the FastAPI application structure.
- Create a stateless inference router to handle incoming classical and quantum predictions.
- Implement the `multipart/form-data` endpoint (`/api/v1/predict`) to ingest images.

## 5. Frontend Application Development
- Build the core UI layout, routing, and file upload widget.
- Build the metrics dashboard to visually compare SVM vs QSVC outputs.
- Mock the API responses so UI development can proceed parallel to backend development.

## 6. System Integration & Smoke Testing
- Connect the Next.js frontend to the FastAPI backend.
- Run end-to-end smoke tests (dummy tensor injections, Qiskit sanity checks) to ensure the system will not crash during live demonstrations.
