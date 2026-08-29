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
        
    def extract(self, image_path: str):
        """
        Extracts features from an image using DenseNet121.
        Returns a tuple: (pooled_features_1d, spatial_features_3d)
        """
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0)  # Add batch dimension
        
        with torch.no_grad():
            spatial_out = self.features(input_tensor) # Shape: (1, 1024, 7, 7)
            # Global Average Pooling
            import torch.nn.functional as F
            pooled_out = F.adaptive_avg_pool2d(spatial_out, (1, 1))
            pooled_out = torch.flatten(pooled_out, 1)
            
        return pooled_out.squeeze(0), spatial_out.squeeze(0)

# Singleton for easy import and usage in FastAPI
extractor = DenseNetFeatureExtractor()
