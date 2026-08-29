import numpy as np
import os
import pickle
from sklearn.decomposition import PCA
from sklearn.svm import SVC
import torch

from src.ml import constants

from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_algorithms.state_fidelities import ComputeUncompute
from qiskit.primitives import StatevectorSampler as Sampler

def train_pca(embeddings: np.ndarray) -> PCA:
    """Trains a PCA model to reduce embeddings to PCA_COMPONENTS dimensions."""
    pca = PCA(n_components=constants.PCA_COMPONENTS)
    pca.fit(embeddings)
    return pca

def construct_quantum_kernel() -> FidelityQuantumKernel:
    """Constructs a ZZFeatureMap and a FidelityQuantumKernel."""
    feature_map = ZZFeatureMap(feature_dimension=constants.PCA_COMPONENTS, reps=2, entanglement='linear')
    
    # We use a primitive Sampler. In production/qiskit_aer, this can be configured 
    # to use AerSimulator, but the base Sampler is sufficient for mathematical validation.
    sampler = Sampler()
    fidelity = ComputeUncompute(sampler=sampler)
    quantum_kernel = FidelityQuantumKernel(fidelity=fidelity, feature_map=feature_map)
    return quantum_kernel

def train_classical_svm(features: np.ndarray, labels: np.ndarray) -> SVC:
    """Trains a pure classical SVC on the PCA features for fair comparison."""
    # Using probability=True so we can extract confidence scores natively
    csvm = SVC(kernel="rbf", probability=True)
    csvm.fit(features, labels)
    return csvm

def train_qsvm(kernel_matrix: np.ndarray, labels: np.ndarray) -> SVC:
    """Trains a classical SVC using the precomputed quantum kernel matrix."""
    qsvm = SVC(kernel="precomputed", probability=True)
    qsvm.fit(kernel_matrix, labels)
    return qsvm

def save_weights(obj, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def load_weights(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    print("Simulating Phase 2 QSVM Training Pipeline...")
    
    # Cap samples to 20 to prevent paging file / OOM issues during testing
    N = 20
    
    print(f"Generating {N} dummy DenseNet embeddings...")
    dummy_embeddings = np.random.rand(N, constants.DENSENET_FEATURES)
    dummy_labels = np.random.randint(0, 2, size=N)
    
    print(f"1. Training PCA from {constants.DENSENET_FEATURES} -> {constants.PCA_COMPONENTS} dimensions...")
    pca = train_pca(dummy_embeddings)
    pca_features = pca.transform(dummy_embeddings)
    
    print("2. Constructing Quantum Kernel...")
    qkernel = construct_quantum_kernel()
    
    print("3. Precomputing Quantum Kernel Matrix (This may take a moment)...")
    kernel_matrix = qkernel.evaluate(x_vec=pca_features)
    
    print("4a. Training Classical SVM (RBF) for comparison...")
    csvm = train_classical_svm(pca_features, dummy_labels)

    print("4b. Training QSVM...")
    qsvm = train_qsvm(kernel_matrix, dummy_labels)
    
    print("5. Saving weights to disk...")
    save_weights(pca, "src/ml/weights/pca.pkl")
    save_weights(qsvm, "src/ml/weights/qsvm.pkl")
    save_weights(csvm, "src/ml/weights/csvm.pkl")
    # Save the training PCA features so we can evaluate new samples against them in production
    save_weights(pca_features, "src/ml/weights/training_pca_features.pkl")
    
    print("Training complete.")
