# Interface Contracts

## 1. REST API Contract (Frontend to Backend)

### `POST /api/v1/predict`
**Content-Type:** `multipart/form-data`
**Payload:** `file` (Binary Image File - JPEG/PNG)
**Query Parameters:** `?dry_run=true|false` (Optional)

**Response:** `200 OK` `application/json`
```json
{
  "status": "success",
  "metadata": {
    "image_id": "uuid-string",
    "processing_time_ms": 1250
  },
  "results": {
    "classical": {
      "model": "RBF-SVM",
      "prediction": "TB Positive",
      "confidence": 0.89,
      "inference_time_ms": 15
    },
    "quantum": {
      "model": "QSVM (ZZFeatureMap, 8 qubits)",
      "prediction": "TB Positive",
      "confidence": 0.85,
      "inference_time_ms": 1150,
      "circuit_depth": 24
    }
  },
  "visualizations": {
    "segmentation_mask_url": "/static/masks/uuid-string.png",
    "gradcam_heatmap_url": "/static/heatmaps/uuid-string.png"
  }
}
```
*Note: Frontend agents must build UI strictly based on this JSON schema.*
