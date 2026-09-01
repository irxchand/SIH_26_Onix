# Data Schemas

## 1. Image Tensors
- **Raw Input:** `[1, 3, 224, 224]` Float32 tensor (Normalized).
- **Segmentation Mask:** `[1, 1, 224, 224]` Binary tensor.

## 2. Feature Vectors
- **DenseNet121 Output:** `[1, 1024]` Float32 vector.
- **PCA Output:** `[1, 8]` Float32 vector (strictly separated fit on training data).

## 3. Quantum Kernel Matrix
- **Training Kernel Matrix:** `[M, M]` Float64 array (pre-computed and loaded to RAM, where M is the training set size).
- **Inference Kernel Array:** `[1, M]` Float64 array (computed dynamically at runtime for the uploaded image).
