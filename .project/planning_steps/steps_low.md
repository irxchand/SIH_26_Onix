# Low-Level Steps (The Execution View)

## 1. System & Repository Initialization
1. Run `uv venv` and activate the Python virtual environment.
2. Create `requirements.txt` containing `fastapi`, `uvicorn`, `torch`, `torchvision`, `scikit-learn`, `qiskit`, `qiskit-machine-learning`, and `python-multipart`.
3. Run `pip install -r requirements.txt`.
4. Run `npx create-next-app@latest frontend --typescript --tailwind --eslint`.
5. Install UI dependencies: `npm install framer-motion lucide-react clsx tailwind-merge`.

## 2. Data Engineering & Preprocessing Pipeline
6. Write `download_datasets.py` to programmatically fetch CXR images.
7. Write `preprocess.py`: load images, resize to 224x224, convert to grayscale/RGB, normalize pixels to `[0, 1]`.
8. Write `segmentation.py`: load a pretrained UNet, run inference on the image, apply a binary threshold, and multiply the mask with the original image.
9. Write `feature_extraction.py`: load `torchvision.models.densenet121(pretrained=True)`, remove the final classification head, run a forward pass to obtain a `[1, 1024]` tensor.
10. Execute the preprocessing pipeline on all images and save features as `.npy` (NumPy) arrays.
11. Write `train_test_split.py`: split datasets (80/20) ensuring no patient data overlaps between sets.

## 3. Machine Learning Pipeline
12. Write `train_pca.py`: load training features, initialize `StandardScaler` and `PCA(n_components=8)`. Fit *only* on training data. Transform both train and test data. Save PCA and Scaler objects using `joblib`.
13. Write `train_svm.py`: load the 8D training data, train `SVC(kernel='rbf')`, and evaluate on test data. Save the SVM model to disk.
14. Write `train_qsvm.py`: initialize `ZZFeatureMap(feature_dimension=8, reps=2, entanglement='linear')`.
15. Setup `FidelityQuantumKernel` using Qiskit's `AerSimulator`.
16. Compute the $N \times N$ training kernel matrix.
17. Train `QSVC` using the pre-computed kernel matrix. Evaluate on the test set. Save the QSVC model and the kernel matrix to disk.

## 4. Backend API Development
18. Create `backend/main.py`.
19. Define a FastAPI `@app.lifespan` hook to load the UNet, DenseNet121, PCA scaler, SVM, and QSVC into memory exactly once on startup.
20. Create Pydantic schemas corresponding to the `06_interfaces.md` JSON response format.
21. Implement the `POST /api/v1/predict` endpoint:
    - Read uploaded file bytes.
    - Convert bytes to PIL Image -> PyTorch Tensor.
    - Sequentially run `segmentation(tensor)` -> `extract_features(tensor)` -> `pca.transform(tensor)`.
    - Branch 1: execute `svm.predict(features)`.
    - Branch 2: calculate quantum kernel fidelity between the new feature and the saved training set, then execute `qsvc.predict(features)`.
    - Map the classical and quantum results to the Pydantic schema and return as JSON.

## 5. Frontend Application Development
22. Create a Next.js API client `src/lib/api.ts` utilizing `fetch` to handle interactions with the FastAPI backend.
23. Create `src/components/UploadWidget.tsx` utilizing the HTML5 File API for drag-and-drop support.
24. Create `src/components/ResultsDashboard.tsx` to parse and state-manage the API JSON response.
25. Create `src/components/MetricCard.tsx` to display classical vs quantum inference times, confidence scores, and circuit depth.
26. Create `src/components/HeatmapViewer.tsx` to overlay the returned segmentation mask/heatmap over the original CXR image.
27. Update `src/app/page.tsx` to stitch the layout components together.

## 6. System Integration & Smoke Testing
28. Add CORS middleware in FastAPI to accept requests from `http://localhost:3000`.
29. Write `tests/test_dummy_pipeline.py`: send `torch.randn(1, 3, 224, 224)` through the FastAPI pipeline functions directly to verify there are no tensor shape mismatches.
30. Write `tests/test_qiskit_sanity.py`: run a basic 1-qubit circuit to verify `AerSimulator` is accessible and functional on the host machine.
31. Start the backend (`uvicorn main:app --reload`) and frontend (`npm run dev`) servers locally.
32. Perform a manual end-to-end test: upload a test CXR image via the UI and verify a successful JSON response and visual render.
