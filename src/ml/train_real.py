import os
import argparse
import numpy as np
from pathlib import Path

from src.ml.feature_extraction import extractor
from src.ml import constants
from src.ml.qsvm import (
    train_pca,
    construct_quantum_kernel,
    train_classical_svm,
    train_qsvm,
    save_weights
)

def extract_features_from_directory(directory: str, label: int):
    print(f"Scanning {directory} for images (label={label})...")
    features_list = []
    labels_list = []
    
    valid_extensions = {".jpg", ".jpeg", ".png"}
    
    path = Path(directory)
    if not path.exists():
        print(f"Warning: Directory {directory} does not exist.")
        return features_list, labels_list
        
    for file_path in path.rglob("*"):
        if file_path.suffix.lower() in valid_extensions:
            try:
                print(f"  Extracting features from {file_path.name}...")
                pooled_features, _ = extractor.extract(str(file_path))
                features_list.append(pooled_features.numpy())
                labels_list.append(label)
            except Exception as e:
                print(f"  Error processing {file_path.name}: {e}")
                
    return features_list, labels_list

def main():
    parser = argparse.ArgumentParser(description="Train Quantum and Classical SVMs on real X-Ray images.")
    parser.add_argument("--healthy", type=str, default="data/dataset/healthy", help="Path to folder containing healthy X-Rays")
    parser.add_argument("--anomaly", type=str, default="data/dataset/anomaly", help="Path to folder containing anomaly X-Rays")
    args = parser.parse_args()

    print("--- REAL CLINICAL QSVM TRAINING PIPELINE ---")
    
    # 1. Feature Extraction
    print("\nPhase 1: Deep Feature Extraction (DenseNet121)")
    healthy_features, healthy_labels = extract_features_from_directory(args.healthy, label=0)
    anomaly_features, anomaly_labels = extract_features_from_directory(args.anomaly, label=1)
    
    all_features = healthy_features + anomaly_features
    all_labels = healthy_labels + anomaly_labels
    
    if len(all_features) < 2:
        print("Error: Not enough images found. You need at least one image in each class to train.")
        return
        
    X = np.vstack(all_features)
    y = np.array(all_labels)
    
    # Shuffle
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    X = X[indices]
    y = y[indices]
    
    print(f"Successfully extracted 1024-D embeddings for {len(X)} total images.")
    
    # 2. PCA Compression
    print(f"\nPhase 2: Training PCA from {constants.DENSENET_FEATURES} -> {constants.PCA_COMPONENTS} dimensions...")
    pca = train_pca(X)
    pca_features = pca.transform(X)
    
    # 3. Quantum Kernel Construction
    print("\nPhase 3: Constructing and Evaluating Quantum Kernel Matrix...")
    qkernel = construct_quantum_kernel()
    kernel_matrix = qkernel.evaluate(x_vec=pca_features)
    
    # 4. SVM Training
    print("\nPhase 4: Training SVM Models...")
    print("  -> Training Classical SVM (RBF)...")
    csvm = train_classical_svm(pca_features, y)
    
    print("  -> Training Quantum SVM...")
    qsvm = train_qsvm(kernel_matrix, y)
    
    # 5. Saving Weights
    print("\nPhase 5: Exporting clinically grounded weights...")
    save_weights(pca, "src/ml/weights/pca.pkl")
    save_weights(qsvm, "src/ml/weights/qsvm.pkl")
    save_weights(csvm, "src/ml/weights/csvm.pkl")
    save_weights(pca_features, "src/ml/weights/training_pca_features.pkl")
    
    print("\nSUCCESS! The pipeline is now grounded in real clinical data.")
    print("The backend will automatically use these authentic weights upon next restart.")

if __name__ == "__main__":
    main()
