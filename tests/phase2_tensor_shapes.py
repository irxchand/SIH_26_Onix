import numpy as np
from src.ml import constants
from src.ml.qsvm import train_pca

def test_pca_tensor_shape():
    N = 10
    # Simulate DenseNet feature extraction (N, 1024)
    raw_embeddings = np.random.rand(N, constants.DENSENET_FEATURES)
    assert raw_embeddings.shape == (N, 1024), f"Expected (N, 1024), got {raw_embeddings.shape}"
    
    pca = train_pca(raw_embeddings)
    pca_features = pca.transform(raw_embeddings)
    
    assert pca_features.shape == (N, constants.PCA_COMPONENTS), f"Expected (N, {constants.PCA_COMPONENTS}), got {pca_features.shape}"
    assert pca_features.shape[1] == 8, "Strict enforcement: PCA output must be exactly 8 dimensions to fit ZZFeatureMap."
