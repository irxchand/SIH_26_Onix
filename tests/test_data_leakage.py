import os
import pytest

def test_data_directories_exist_and_disjoint():
    """
    Ensures that if the data directories exist, the train and test folders do not overlap.
    This is an anti-leakage test to prevent testing on training data.
    """
    train_dir = "data/train"
    test_dir = "data/test"
    
    # If the directories haven't been created yet by E2, pass the test
    if not os.path.exists(train_dir) or not os.path.exists(test_dir):
        pytest.skip("Data directories not yet created.")
        
    train_files = set(os.listdir(train_dir))
    test_files = set(os.listdir(test_dir))
    
    # The intersection should be absolutely empty
    intersection = train_files.intersection(test_files)
    
    assert len(intersection) == 0, f"DATA LEAKAGE DETECTED! {len(intersection)} files exist in both train and test sets: {intersection}"

def test_qiskit_pca_dimensions():
    """
    Ensures the PCA constraint is small enough for the quantum simulator.
    """
    from src.ml.constants import PCA_COMPONENTS
    assert PCA_COMPONENTS <= 16, "PCA components must be <= 16 to avoid crashing the local Qiskit simulator."
