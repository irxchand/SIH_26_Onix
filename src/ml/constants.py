# Mathematical Bounds and Constants for Quantum/Classical ML

# Qiskit Simulator Constraints
# High dimensions will crash the local simulator. 
# We strictly enforce PCA reduction to this number of components before feeding into the ZZFeatureMap.
PCA_COMPONENTS = 8

# Image Constraints
TARGET_IMAGE_SIZE = (224, 224) # Standard for DenseNet121

# Deep Feature Extraction
DENSENET_FEATURES = 1024 # DenseNet121 outputs 1024 features before the classification head
