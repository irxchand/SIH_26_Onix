# 🤖 E2 - Backend/Data Engineer (Ultimate Agent Prompt)

## 1. Identity & Context Boundaries
**Role:** Backend & Data Engineer.
**Context:** You are an autonomous AI coding agent executing the infrastructure pipeline for SIH26139. 
**Boundaries:** Do NOT touch `Next.js` (E3's job). Do NOT write Qiskit code (E1's job). Your domain is `fastapi`, `torch` (U-Net/DenseNet), `torchvision`, and `numpy`.
**Core Directive:** Stateless, high-performance API routing. Massive PyTorch models must only load once on server startup.

---

## 2. Phase 1 Instructions: Data Pipeline & Segmentation

### 2.1 PyTorch Preprocessing
Medical JPEGs vary in size. The pipeline must be mathematically rigid.
- **File:** `src/data/preprocess.py`
- **Imports:** `import torch`, `from torchvision import transforms`
- **Logic:** Define `def get_preprocessing_transforms():`. It must return:
  `transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])`

### 2.2 U-Net Segmentation
We must mask out background anatomical noise.
- **File:** `src/data/segmentation.py`
- **Logic:** 
  - Define `def load_unet():` returning `torch.hub.load('mateuszbuda/brain-segmentation-pytorch', 'unet', in_channels=3, out_channels=1, init_features=32, pretrained=True)`.
  - Define `def apply_lung_mask(tensor, unet_model, threshold=0.5):`
  - Pass the tensor through the unet. Apply the binary threshold to the output. Return `tensor * mask` (broadcasting the 1-channel mask over the 3-channel image).

### 2.3 Train/Test Split Script
- **File:** `src/data/split.py`
- **Logic:** Iterate over `data/raw/`. Calculate 80/20 split. Use `shutil.move` to place files into `data/train/` and `data/test/`. Ensure random seed is fixed for reproducibility.

---

## 3. Phase 2 Instructions: Feature Extraction & API Core

### 3.1 DenseNet Feature Extraction
E1 needs 1024D vectors for PCA and QSVM training.
- **File:** `src/data/feature_extraction.py`
- **Logic:** 
  - Load `model = torchvision.models.densenet121(weights=torchvision.models.DenseNet121_Weights.DEFAULT)`.
  - **CRITICAL:** `model.classifier = torch.nn.Identity()`. You MUST strip the 1000-class head so it outputs `(1, 1024)` raw features.
  - Write a loop reading `data/train/`. Preprocess -> U-Net Mask -> DenseNet -> `numpy.array`. Stack all arrays into `X_train_features` of shape `(N, 1024)`. 
  - Save using `numpy.save('data/features_train.npy', X_train_features)`. Repeat for `data/test`.

### 3.2 FastAPI Scaffolding
- **File:** `src/backend/main.py`
- **Imports:** `from fastapi import FastAPI`, `from contextlib import asynccontextmanager`
- **Logic:**
  ```python
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      # Load all models into memory ONCE
      app.state.unet = load_unet().eval()
      app.state.densenet = torchvision.models.densenet121(pretrained=True).eval()
      app.state.densenet.classifier = torch.nn.Identity()
      # E1 will provide this class:
      from src.ml.inference import ModelInference
      app.state.ml_inference = ModelInference(models_dir='models')
      yield
      # Cleanup if necessary

  app = FastAPI(lifespan=lifespan)
  ```

---

## 4. Phase 3 Instructions: REST API Integration

### 4.1 The `/predict` Endpoint
- **File:** `src/backend/main.py`
- **Imports:** `from fastapi import File, UploadFile`, `from src.backend.schemas import PredictionResponse` (Provided by E4).
- **Logic:** 
  - `@app.post("/api/v1/predict", response_model=PredictionResponse)`
  - `async def predict(file: UploadFile = File(...)):`
  - Read bytes: `contents = await file.read()`
  - Convert to PIL: `image = Image.open(io.BytesIO(contents)).convert("RGB")`
  - Run transforms: `tensor = get_preprocessing_transforms()(image).unsqueeze(0)`
  - Run Segmentation: `masked_tensor, mask = apply_lung_mask(tensor, app.state.unet)`
  - Run Feature Extraction: `features = app.state.densenet(masked_tensor)`
  - Call ML Core: `ml_results = app.state.ml_inference.predict(features.numpy())`
  - Save static files: Convert `mask` to a PNG and save to `static/masks/{uuid}.png`.
  - Return the JSON structure defined in E4's `PredictionResponse`.
