"""
Feature extractor module — supports DenseNet121, EfficientNet-B0, ConvNeXt-Tiny.
Handles whole-CXR and lung-masked/cropped representations.
"""
import torch
import torch.nn.functional as F
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path
from typing import Literal, Optional

# ── ImageNet normalization stats ────────────────────────────────────────────
_IMAGENET_MEAN = [0.485, 0.456, 0.406]
_IMAGENET_STD  = [0.229, 0.224, 0.225]

# ── Available encoder registry ──────────────────────────────────────────────
ENCODER_CONFIGS = {
    "densenet121": {
        "loader": lambda: models.densenet121(weights=models.DenseNet121_Weights.DEFAULT),
        "feature_fn": lambda m, x: _densenet_feats(m, x),
        "out_dim": 1024,
    },
    "efficientnet_b0": {
        "loader": lambda: models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT),
        "feature_fn": lambda m, x: _efficientnet_feats(m, x),
        "out_dim": 1280,
    },
    "convnext_tiny": {
        "loader": lambda: models.convnext_tiny(weights=models.ConvNeXt_Tiny_Weights.DEFAULT),
        "feature_fn": lambda m, x: _convnext_feats(m, x),
        "out_dim": 768,
    },
}

def _densenet_feats(model, x):
    out = model.features(x)
    out = F.adaptive_avg_pool2d(out, (1, 1))
    return torch.flatten(out, 1)

def _efficientnet_feats(model, x):
    out = model.features(x)
    out = model.avgpool(out)
    return torch.flatten(out, 1)

def _convnext_feats(model, x):
    out = model.features(x)
    out = model.avgpool(out)
    return torch.flatten(out, 1)


class CXRFeatureExtractor:
    """
    Multi-encoder CXR feature extractor with lung masking support.

    representation:
      'whole'   - Full CXR resized to 224x224. No anatomical restriction.
      'masked'  - GROUND-TRUTH REFERENCE: Background zeroed using Montgomery
                  expert-annotated manual lung masks. NOT automated segmentation.
                  In experiment logs this is labelled GT_LUNG_MASKED.
      'cropped' - GROUND-TRUTH REFERENCE: Tight bounding-box crop using manual
                  lung masks, resized to 224x224. NOT automated segmentation.
                  In experiment logs this is labelled GT_LUNG_CROPPED.

    IMPORTANT: 'masked' and 'cropped' modes require expert-annotated lung mask files
    at data/datasets/montgomery/MontgomerySet/ManualMask/{leftMask,rightMask}/*.png.
    If masks are absent the representation silently falls back to 'whole'.
    """

    def __init__(
        self,
        encoder: str = "densenet121",
        representation: Literal["whole", "masked", "cropped"] = "whole",
        clahe: bool = True,
    ):
        if encoder not in ENCODER_CONFIGS:
            raise ValueError(f"Unknown encoder: {encoder}. Choose from {list(ENCODER_CONFIGS)}")

        cfg = ENCODER_CONFIGS[encoder]
        self.model = cfg["loader"]()
        self.model.eval()
        self.feature_fn = cfg["feature_fn"]
        self.out_dim = cfg["out_dim"]
        self.encoder_name = encoder
        self.representation = representation
        self.clahe = clahe

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=_IMAGENET_MEAN, std=_IMAGENET_STD),
        ])

    def _apply_clahe(self, pil_img: Image.Image) -> Image.Image:
        """Apply CLAHE via OpenCV for contrast enhancement."""
        try:
            import cv2
            gray = np.array(pil_img.convert("L"))
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            return Image.fromarray(enhanced).convert("RGB")
        except ImportError:
            return pil_img

    def _get_lung_mask(self, image_path: str) -> Optional[np.ndarray]:
        """Load Montgomery manual lung mask if it exists."""
        p = Path(image_path)
        stem = p.stem  # e.g. MCUCXR_0021_0
        dataset_base = Path("data/datasets/montgomery/MontgomerySet")
        left_mask_path  = dataset_base / "ManualMask" / "leftMask"  / f"{stem}.png"
        right_mask_path = dataset_base / "ManualMask" / "rightMask" / f"{stem}.png"

        if not (left_mask_path.exists() and right_mask_path.exists()):
            return None

        left  = np.array(Image.open(left_mask_path).convert("L"))
        right = np.array(Image.open(right_mask_path).convert("L"))
        combined = ((left > 0) | (right > 0)).astype(np.uint8) * 255
        return combined

    def extract(self, image_path: str) -> torch.Tensor:
        img = Image.open(image_path).convert("RGB")

        if self.clahe:
            img = self._apply_clahe(img)

        if self.representation in ("masked", "cropped"):
            mask = self._get_lung_mask(image_path)
            if mask is not None:
                mask_resized = np.array(
                    Image.fromarray(mask).resize(img.size, Image.NEAREST)
                ) > 0

                if self.representation == "masked":
                    img_arr = np.array(img).astype(np.float32)
                    bg_mean = img_arr[~mask_resized].mean() if (~mask_resized).any() else 0.0
                    img_arr[~mask_resized] = bg_mean
                    img = Image.fromarray(img_arr.clip(0, 255).astype(np.uint8))

                elif self.representation == "cropped":
                    rows = np.where(mask_resized.any(axis=1))[0]
                    cols = np.where(mask_resized.any(axis=0))[0]
                    if len(rows) > 0 and len(cols) > 0:
                        pad = 10
                        r0, r1 = max(0, rows[0]-pad), min(img.height, rows[-1]+pad)
                        c0, c1 = max(0, cols[0]-pad), min(img.width, cols[-1]+pad)
                        img = img.crop((c0, r0, c1, r1))

        tensor = self.transform(img).unsqueeze(0)
        with torch.no_grad():
            feats = self.feature_fn(self.model, tensor)
        return feats.squeeze(0)

    def extract_with_cam(self, image_path: str):
        """Extract features and return simple Grad-CAM simulated spatial coordinates."""
        if self.encoder_name != "densenet121":
            raise ValueError("CAM extraction currently only supported for densenet121")
            
        img = Image.open(image_path).convert("RGB")
        if self.clahe:
            img = self._apply_clahe(img)
            
        tensor = self.transform(img).unsqueeze(0)
        with torch.no_grad():
            out = self.model.features(tensor) # (1, 1024, 7, 7)
            
            # Global Average Pooling for the 1024-D embedding
            pooled = F.adaptive_avg_pool2d(out, (1, 1))
            feats = torch.flatten(pooled, 1).squeeze(0)
            
            # Simple CAM: average across channels to find anomaly activation
            cam = out.mean(dim=1).squeeze(0) # (7, 7)
            
            # Find argmax
            max_idx = torch.argmax(cam)
            y_idx = float(max_idx // 7)
            x_idx = float(max_idx % 7)
            
            # Map 7x7 grid to 0-100 percent for UI bounding box mapping
            xPercent = (x_idx / 6.0) * 100.0
            yPercent = (y_idx / 6.0) * 100.0
            
        return feats, {"xPercent": xPercent, "yPercent": yPercent, "intensity": float(cam.max())}


# Default backward-compatible extractor (DenseNet, whole CXR)
class DenseNetFeatureExtractor(CXRFeatureExtractor):
    def __init__(self):
        super().__init__(encoder="densenet121", representation="whole", clahe=True)
