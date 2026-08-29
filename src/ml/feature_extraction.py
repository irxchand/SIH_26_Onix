import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from src.ml.constants import TARGET_IMAGE_SIZE

class DenseNetFeatureExtractor:
    def __init__(self):
        # Using default pre-trained weights for DenseNet121
        self.model = models.densenet121(weights=models.DenseNet121_Weights.DEFAULT)
        # We only want the features, not the classification head
        self.features = self.model.features
        self.features.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize(TARGET_IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
        
    def extract(self, image_path: str) -> torch.Tensor:
        """
        Extracts features from an image using DenseNet121.
        Returns a 1D tensor of features (after global average pooling).
        """
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0)  # Add batch dimension
        
        with torch.no_grad():
            out = self.features(input_tensor)
            # Global Average Pooling
            import torch.nn.functional as F
            out = F.adaptive_avg_pool2d(out, (1, 1))
            out = torch.flatten(out, 1)
            
        return out.squeeze(0)

# Singleton for easy import and usage in FastAPI
extractor = DenseNetFeatureExtractor()
