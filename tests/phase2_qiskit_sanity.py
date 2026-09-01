from src.ml.qsvm import construct_quantum_kernel
from src.ml import constants

def test_qiskit_feature_map_dimensions():
    qkernel = construct_quantum_kernel()
    
    # Assert ZZFeatureMap is instantiated with the right number of qubits
    feature_map = qkernel.feature_map
    assert feature_map.num_qubits == constants.PCA_COMPONENTS, f"FeatureMap qubits must match PCA_COMPONENTS ({constants.PCA_COMPONENTS})"
    assert feature_map.num_qubits == 8, "Strict enforcement: FeatureMap must have exactly 8 qubits to avoid OOM."
