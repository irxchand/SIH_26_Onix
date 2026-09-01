"""
src/data/segmentation.py

AUTOMATED SEGMENTATION — Phase 1 Status: NOT IMPLEMENTED

This module is a placeholder for a future automated lung segmentation model.

Current Phase 1 segmentation strategy:
  - For Montgomery dataset studies: expert-annotated manual masks from the dataset
    are used (GT_LUNG_MASKED, GT_LUNG_CROPPED representations).
  - For uploaded studies without masks: Otsu-thresholding via src/ml/segmentation.py
    is used as a rough anatomical approximation (not a trained model prediction).

These are explicitly labeled in the API response confidence field:
  - 1.0 → ground-truth manual mask (Montgomery)
  - 0.0 → Otsu heuristic fallback (no model, no trained inference)

FUTURE WORK:
  A proper pretrained lung segmentation model (e.g., U-Net trained on JSRT/NIH CXR datasets)
  can be integrated here once validated. It must be:
  - Evaluated on a held-out segmentation benchmark before use
  - Labeled as AUTOMATED_SEGMENTATION (not GROUND_TRUTH_REFERENCE)
  - Not mixed with the Montgomery GT masks for the controlled Track B comparisons

  The activate representations would then become:
    AUTO_LUNG_MASKED  — background zeroed using automated mask
    AUTO_LUNG_CROPPED — tight bounding box crop using automated mask

DO NOT:
  - Return dummy masks as if they were real segmentation outputs
  - Label automated masks as ground-truth
  - Use this module in any scientific pipeline until a validated model is in place
"""

# No executable code here — see src/ml/segmentation.py for the active implementation
# (get_montgomery_mask_contours and get_lung_contours_svg)
