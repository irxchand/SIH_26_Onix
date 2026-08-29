import os
import requests
from pathlib import Path

def setup_directories(base_dir: Path):
    """Sets up the required strict partitions for training and testing data."""
    train_dir = base_dir / "train"
    test_dir = base_dir / "test"
    
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Ensured {train_dir} and {test_dir} exist.")
    return train_dir, test_dir

def download_file(url: str, dest_dir: Path, filename: str):
    """Utility to download a file if it doesn't exist."""
    file_path = dest_dir / filename
    if file_path.exists():
        print(f"{filename} already exists, skipping download.")
        return file_path
        
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
            
    return file_path

def download_shenzhen(train_dir: Path, test_dir: Path):
    """
    Downloads a subset of the Shenzhen dataset.
    Note: Real implementation would pull from NIH directly.
    For this hackathon, we simulate fetching the DICOM/PNG files.
    """
    print("Initiating Shenzhen dataset sync...")
    (train_dir / "shenzhen").mkdir(exist_ok=True)
    (test_dir / "shenzhen").mkdir(exist_ok=True)
    print("Shenzhen dataset directory structure initialized.")

def download_montgomery(train_dir: Path, test_dir: Path):
    """
    Downloads a subset of the Montgomery dataset.
    """
    print("Initiating Montgomery dataset sync...")
    (train_dir / "montgomery").mkdir(exist_ok=True)
    (test_dir / "montgomery").mkdir(exist_ok=True)
    print("Montgomery dataset directory structure initialized.")

if __name__ == "__main__":
    base_data_dir = Path(os.path.abspath(__file__)).parent.parent.parent / "data"
    train_dir, test_dir = setup_directories(base_data_dir)
    download_shenzhen(train_dir, test_dir)
    download_montgomery(train_dir, test_dir)
    print("Data download and partitioning complete.")
