# UI Technical Debt: Feature-by-Feature Endpoint & Error Specification

This document catalogs **every** interactive feature in the frontend, the backend endpoint it requires, and the logical errors that must be handled. This is the single source of truth for transitioning the Phase 1 demo into a live system.

---

## 1. MEASURE (Caliper & CTR Checklist)

### Current State
- User clicks 6 anatomical landmarks on the X-ray canvas. A checklist in the right panel tracks progress.
- Once heart and chest boundaries are set, the UI calculates CTR using a **fake pixel-to-mm multiplier** (`* 4.2`).
- A popover appears with H/C/R values and a text area for clinical notes.
- Clicking "Save" sets a local boolean (`savedMeasurementIssue`). **All data is lost on refresh.**

### Required Endpoints
| Method | Route | Payload | Response |
|--------|-------|---------|----------|
| `POST` | `/api/v1/studies/{id}/measurements` | `{ points: [{id, x, y}], hDistMm, cDistMm, ratio, note }` | `{ measurementId, savedAt }` |
| `GET` | `/api/v1/studies/{id}/measurements` | — | `[ { measurementId, points, ratio, note, savedAt } ]` |

### Logical Errors to Handle
- **Incomplete points array** (< 6 points): Frontend must block the Save button. Backend must reject with `422`.
- **Division by zero**: If `cDistMm === 0` (chest points overlap), frontend must display an error instead of `Infinity%`.
- **Out-of-bounds coordinates**: Points with `x > 100` or `y > 100` must be clamped or rejected.
- **Real pixel spacing**: The multiplier `* 4.2` must be replaced with actual DICOM pixel spacing from backend metadata (`GET /api/v1/studies/{id}/metadata`).

---

## 2. SEGMENT (U-Net Lung Contours)

### Current State
- Two hardcoded SVG `<path>` elements render approximate lung contour shapes.
- These paths are **static** and identical for every X-ray image.

### Required Endpoints
| Method | Route | Payload | Response |
|--------|-------|---------|----------|
| `GET` | `/api/v1/studies/{id}/segmentation` | — | `{ leftLung: "M 25 30 C...", rightLung: "M 45 30 C...", confidence: 0.94 }` |

### Logical Errors to Handle
- **Empty masks**: If the U-Net returns no contours (e.g., non-chest image), the frontend must display "No segmentation available" instead of rendering nothing.
- **Malformed SVG paths**: Invalid path strings from the backend will crash the SVG renderer. Frontend must validate path syntax before rendering.
- **Dimension mismatch**: The mask coordinates must be normalized to the same `0-100%` coordinate space the canvas uses. If the backend returns pixel coordinates, the frontend must scale them.

---

## 3. EVIDENCE (Anomaly Pins & Observations)

### Current State
- `mockEvidence` provides hardcoded pin locations and descriptions.
- Each pin has a floating dialog with region, signal, and a text input for observation notes.
- **Notes are stored in local React state and lost on refresh.**

### Required Endpoints
| Method | Route | Payload | Response |
|--------|-------|---------|----------|
| — | `/api/v1/predict` | (existing) | Must include `evidence: [{ id, region, confidence, signal, xPercent, yPercent }]` |
| `POST` | `/api/v1/studies/{id}/evidence/{evidenceId}/notes` | `{ note: string }` | `{ noteId, savedAt }` |
| `GET` | `/api/v1/studies/{id}/evidence` | — | Full evidence array with saved notes |

### Logical Errors to Handle
- **Missing coordinates**: If `xPercent` or `yPercent` is `null`/`undefined`, the pin renders at `(0, 0)` (top-left corner). Must default to hidden or show a warning.
- **Confidence = 0**: A zero-confidence evidence item should not be rendered as a pin — it's noise.
- **Duplicate evidence IDs**: Backend must enforce uniqueness. Frontend must deduplicate before rendering.

---

## 4. QUANTUM (Circuit View & Metrics)

### Current State
- `QuantumCircuitView` renders an animated circuit board that loops during pipeline execution.
- `RightIntelligence` displays **hardcoded** values: `92.4%` classical accuracy, `91.8%` quantum accuracy, `Qubits: 8`, `Depth: 24`.

### Required Endpoints
| Method | Route | Payload | Response |
|--------|-------|---------|----------|
| — | `/api/v1/predict` | (existing) | Must include `{ qubits, circuit_depth, feature_map, simulator, execution_stage }` |

### Logical Errors to Handle
- **Timeout**: QSVM inference may take >30s. The frontend pipeline animation must not hang — implement a maximum wait with a "Retry" option.
- **Simulator fallback**: If the quantum simulator crashes, the backend should return `execution_stage: "FALLBACK_CLASSICAL"` and the frontend must visually indicate this.
- **NaN confidence**: If the QSVM kernel computation fails, confidence may be `NaN`. Frontend must display "N/A" instead.

---

## 5. ACCEPT / REJECT

### Current State
- Two buttons in `RightIntelligence` trigger `alert("Study Accepted")` / `alert("Study Rejected")`.
- No state change, no persistence, no transition.

### Required Endpoints
| Method | Route | Payload | Response |
|--------|-------|---------|----------|
| `POST` | `/api/v1/studies/{id}/status` | `{ status: "ACCEPTED" \| "REJECTED", reviewedBy: string }` | `{ updatedAt }` |

### Logical Errors to Handle
- **Race condition**: Another radiologist may have already accepted/rejected. Backend must return `409 Conflict` and frontend must show a "Study already reviewed" modal.
- **Post-action transition**: After accepting/rejecting, the UI should transition back to the Queue view and update the study's status badge.
- **Undo**: Consider a 5-second undo window before the POST is sent.

---

## 6. SCAN (Pan/Zoom & Backend Calibration)

### Current State
- The SCAN tool shows a placeholder string `[SCANNING ACTIVE]: Image grid calibration ready`.
- No interactive behavior is implemented.

### Required Implementation (Hybrid — per user instruction: "TRY BOTH")

**Frontend-only (Pan/Zoom):**
- Click-and-drag to pan the image within the viewport.
- Scroll wheel to zoom (already partially implemented via `zoomLevel` state).
- Double-click to reset to default view.

**Backend calibration:**
| Method | Route | Payload | Response |
|--------|-------|---------|----------|
| `POST` | `/api/v1/studies/{id}/calibrate` | `{ brightness, contrast, sharpness, windowCenter, windowWidth }` | `{ calibratedImageUrl }` |

### Logical Errors to Handle
- **Zoom bounds**: Prevent zooming below `0.25x` or above `4.0x` (currently `0.5` to `2.0`).
- **Pan out of bounds**: Clamp the pan offset so the image never fully leaves the viewport.
- **Calibration failure**: If backend returns error, keep the frontend filters as-is and show a warning.

---

## 7. ANNOTATE (Freehand Drawing & Markers)

### Current State
- The ANNOTATE tool shows a placeholder string `[ANNOTATE MODE]: Visual markup active`.
- No interactive behavior is implemented.

### Required Implementation (Hybrid — freehand + text markers)

**Frontend:**
- Freehand SVG `<polyline>` drawing on the canvas using mouse events.
- Right-click to drop a text marker with a label input.
- Color picker for annotation pen color.

**Backend:**
| Method | Route | Payload | Response |
|--------|-------|---------|----------|
| `POST` | `/api/v1/studies/{id}/annotations` | `{ type: "freehand" \| "marker", points: [{x,y}], label?, color }` | `{ annotationId, savedAt }` |
| `GET` | `/api/v1/studies/{id}/annotations` | — | `[ { annotationId, type, points, label, color, savedAt } ]` |
| `DELETE` | `/api/v1/studies/{id}/annotations/{annotationId}` | — | `204 No Content` |

### Logical Errors to Handle
- **Empty polyline**: A freehand annotation with < 2 points should not be saved.
- **Excessive points**: A very long freehand stroke may generate thousands of points. Downsample to max ~200 points before saving.
- **Label length**: Text markers must have labels capped at 256 characters.

---

## 8. QUEUE & UPLOAD

### Current State
- `RadiologyQueue` renders from `mockStudies` imported at build time.
- Custom uploads create a local `URL.createObjectURL()` blob.

### Required Endpoints
| Method | Route | Payload | Response |
|--------|-------|---------|----------|
| `GET` | `/api/v1/queue` | `?search=&status=&page=` | `{ studies: Study[], total, page }` |
| `POST` | `/api/v1/upload` | `multipart/form-data: file` | `{ studyId, status: "READY" }` |
| `GET` | `/api/v1/studies/{id}/metadata` | — | `{ pixelSpacing, dimensions, dicomTags }` |

### Logical Errors to Handle
- **Invalid file type**: Only accept `image/jpeg`, `image/png`, and `application/dicom`. Reject others with a user-facing error.
- **File size limit**: Cap at 50MB. Show progress bar for large uploads.
- **Empty queue**: Display a meaningful empty state, not a blank table.
- **Pagination**: The queue must support pagination when the study count exceeds ~50.

---

## Summary: All Required Endpoints

| # | Method | Route | Phase |
|---|--------|-------|-------|
| 1 | `GET` | `/api/v1/queue` | Phase 2 |
| 2 | `POST` | `/api/v1/upload` | Phase 2 |
| 3 | `GET` | `/api/v1/studies/{id}/metadata` | Phase 2 |
| 4 | `GET` | `/api/v1/studies/{id}/segmentation` | Phase 2 |
| 5 | `POST` | `/api/v1/predict` | Phase 2 (exists, must expand payload) |
| 6 | `POST` | `/api/v1/studies/{id}/measurements` | Phase 3 |
| 7 | `GET` | `/api/v1/studies/{id}/measurements` | Phase 3 |
| 8 | `POST` | `/api/v1/studies/{id}/evidence/{evidenceId}/notes` | Phase 3 |
| 9 | `GET` | `/api/v1/studies/{id}/evidence` | Phase 3 |
| 10 | `POST` | `/api/v1/studies/{id}/status` | Phase 3 |
| 11 | `POST` | `/api/v1/studies/{id}/calibrate` | Phase 3 |
| 12 | `POST` | `/api/v1/studies/{id}/annotations` | Phase 3 |
| 13 | `GET` | `/api/v1/studies/{id}/annotations` | Phase 3 |
| 14 | `DELETE` | `/api/v1/studies/{id}/annotations/{annotationId}` | Phase 3 |
