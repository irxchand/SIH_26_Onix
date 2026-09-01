# 🧑‍💻 E2 - Backend/Data Engineer (Deep Execution & Validation Guide)

## 1. Core Philosophy & Role Definition
As the Backend & Data Engineer, you own the infrastructure pipeline. You are responsible for ensuring that raw image data is scientifically prepared for E1's ML models, and you are responsible for serving those models through a lightning-fast FastAPI server.

**The inherent problem you are solving:** Medical data is messy. If E1's quantum models are fed un-masked chest X-rays, the DenseNet will extract features from the background (shoulders, medical tubing, etc.) instead of the lung tissue. You must forcefully slice out the noise using a U-Net. Secondly, PyTorch and Qiskit models take seconds to load into memory. If your FastAPI server loads them on every HTTP request, the UI will hang for 10+ seconds per click. You must manage state at the ASGI server level.

Your AI Agent can scaffold FastAPI instantly, but it often hallucinates REST boundaries or forgets to manage PyTorch memory correctly. You must strictly validate its architectural choices.

---

## 2. Phase 1: Data Pipeline & Segmentation Validation

### The Objective
Transform messy JPEGs into strictly normalized PyTorch Tensors, run them through a U-Net, apply a binary threshold mask, and separate them into Train/Test folders.

### What to Manually Check & Validate
1. **U-Net Mask Quality:** 
   - *Detail Check:* The agent will download a pre-trained PyTorch U-Net (e.g., from `torch.hub`). It will run inference and apply a threshold (e.g., `0.5`) to create a binary mask.
   - *Action:* Look at the output images saved in `data/train/`. If the lungs are completely blacked out, the threshold is too high, or the tensor normalization (`[0.485, 0.456, 0.406]`) was applied incorrectly before the U-Net. 
2. **Train/Test Isolation:**
   - *Detail Check:* Deep learning is useless if data leaks. Ensure the script physically moves 80% of files to `data/train` and 20% to `data/test`. The agent must not just create soft links or CSV mappings; physically isolate them to prevent E1's agents from accidentally loading test data during PCA.

### Agent Prompts (Phase 1)
**Initialization Prompt:**
> "Agent, I am E2, the Backend/Data Engineer. Load your system directives from `E2_Backend_Data_Engineer_AGENT_PROMPT.md`. We are executing Phase 1. Your task is to build the PyTorch preprocessing transform (Resize 224, Normalize), the U-Net segmentation wrapper (threshold=0.5), and a script to physically split `data/raw` into `data/train` and `data/test`. Stop when done. Do not proceed to Phase 2 until I review the masked images."

**Correction Prompt (If U-Net outputs garbage):**
> "The U-Net segmentation mask is completely blank. This usually means the input tensor was normalized with ImageNet stats *before* the U-Net, but this specific U-Net expects un-normalized `[0,1]` float tensors. Refactor `segmentation.py` to run U-Net on the base tensor, multiply the mask, and *then* apply the ImageNet normalization."

---

## 3. Phase 2: Feature Extraction & API Core Validation

### The Objective
Run all masked images through DenseNet121 (stripping the final classification layer) to generate the `(1, 1024)` vectors E1 needs. Then, build the FastAPI shell.

### What to Manually Check & Validate
1. **DenseNet Head Stripping:**
   - *Detail Check:* The agent must load `torchvision.models.densenet121(pretrained=True)`. By default, this outputs `(1, 1000)` probabilities. The agent MUST delete or bypass the `classifier` layer so it outputs `(1, 1024)` raw features. 
   - *Validation:* Inspect `features_train.npy` shape. If it's `(N, 1000)`, the agent failed.
2. **FastAPI Lifespan Memory Management:**
   - *Detail Check:* Open `src/backend/main.py`. The agent MUST use `@asynccontextmanager def lifespan(app: FastAPI):`. 
   - *Validation:* Inside the lifespan block, you must see the U-Net, DenseNet, and E1's `ModelInference` class instantiated and assigned to `app.state`. If you see them instantiated globally at the top of the file, or inside a route, reject it. Global instantiation breaks Uvicorn multi-worker setups, and route instantiation causes 10-second request latency.

### Agent Prompts (Phase 2)
**Execution Prompt:**
> "Agent, proceed to Phase 2. Build the DenseNet121 extractor, ensuring you strip the classifier head so it yields exactly 1024 features. Loop through `data/train` and `data/test` and save `.npy` arrays. Then, scaffold `main.py` using FastAPI. You MUST load the PyTorch models and E1's `ModelInference` strictly inside the `@asynccontextmanager def lifespan(app: FastAPI):` hook and attach them to `app.state`. Do not write the `/predict` route yet."

---

## 4. Phase 3: REST API Integration Validation

### The Objective
Write the `POST /api/v1/predict` endpoint. It must accept an image, pipe it through the state models, and return the Pydantic JSON schema defined by E4.

### What to Manually Check & Validate
1. **The Request Pipe:**
   - *Detail Check:* Does the endpoint accept `file: UploadFile = File(...)`? Does it properly await the byte reading? Does it convert bytes to a PIL Image before passing it to the preprocessor?
2. **Grad-CAM Hooking:**
   - *Detail Check:* The agent must register a PyTorch forward hook on the final dense block of the DenseNet to generate the Grad-CAM heatmap. This is complex.
   - *Validation:* If the Grad-CAM crashes with a "requires_grad" error, it means the agent called `torch.no_grad()` globally. The Grad-CAM feature requires gradients. Ensure `torch.no_grad()` is strictly managed around the inference calls, but Grad-CAM is allowed to compute the activation gradients.

### Agent Prompts (Phase 3)
**Execution Prompt:**
> "Agent, proceed to Phase 3. Implement the `POST /api/v1/predict` endpoint. Pipe the `UploadFile` bytes to PIL, to preprocess, to U-Net, to DenseNet, to `app.state.ml_inference.predict()`. Implement a Grad-CAM hook on the DenseNet to generate the heatmap. Save the U-Net mask and Heatmap to static URLs, and return the `PredictionResponse` Pydantic model exactly as E4 defined."
