# User Flows

## Flow 1: PoW Demonstration
1. **User** uploads a CXR image via Next.js Frontend.
2. **Frontend** sends `multipart/form-data` to FastAPI `/predict` endpoint.
3. **Backend** processes image (Segmentation, DenseNet121, PCA).
4. **Backend** branches inference to SVM and QSVM.
5. **Backend** returns JSON response with predictions, inference times, and visualization URLs.
6. **Frontend** elegantly displays predictions, side-by-side metric charts, and heatmaps.

## Flow 2: Dry-Run Mode (Fallback)
1. **User** activates `dry_run` mode in UI.
2. **Frontend** appends `?dry_run=true` to API request.
3. **Backend** returns pre-calculated/mocked quantum response to prevent simulator hanging during presentation.
