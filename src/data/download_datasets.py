import os
import requests
import zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def download_range(url, start, end, part_num, dest_dir):
    headers = {'Range': f'bytes={start}-{end}'}
    part_path = dest_dir / f"part_{part_num}"
    r = requests.get(url, headers=headers, stream=True)
    r.raise_for_status()
    with open(part_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
    return part_path

def download_file_multithreaded(url: str, dest_dir: Path, filename: str, num_threads=16) -> Path:
    """Utility to download a file using multiple threads via range requests."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    file_path = dest_dir / filename
    if file_path.exists():
        print(f"{filename} already exists, skipping download.")
        return file_path
        
    print(f"Checking file size for {url}...")
    r = requests.head(url)
    r.raise_for_status()
    total_size = int(r.headers.get('content-length', 0))
    if total_size == 0:
        raise ValueError("Could not determine file size.")
        
    print(f"Total size: {total_size} bytes. Downloading using {num_threads} threads...")
    chunk_size = total_size // num_threads
    ranges = []
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size - 1 if i < num_threads - 1 else total_size - 1
        ranges.append((start, end))
        
    part_paths = [None] * num_threads
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {
            executor.submit(download_range, url, start, end, idx, dest_dir): idx
            for idx, (start, end) in enumerate(ranges)
        }
        for future in futures:
            idx = futures[future]
            try:
                part_paths[idx] = future.result()
                print(f"Thread {idx+1}/{num_threads} finished.")
            except Exception as e:
                print(f"Thread {idx+1} failed: {e}")
                raise e
                
    print("All parts downloaded. Merging files...")
    with open(file_path, 'wb') as outfile:
        for part_path in part_paths:
            with open(part_path, 'rb') as infile:
                # Read and write in chunks to avoid high memory usage
                while True:
                    chunk = infile.read(8192)
                    if not chunk:
                        break
                    outfile.write(chunk)
            part_path.unlink() # delete part file
            
    print(f"Merged successfully into {filename}")
    return file_path

def download_montgomery(base_dir: Path):
    """
    Downloads and extracts the Montgomery County TB dataset.
    """
    dataset_dir = base_dir / "datasets" / "montgomery"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    # If the zip is partially downloaded, remove it to start clean
    zip_name = "NLM-MontgomeryCXRSet.zip"
    zip_path = dataset_dir / zip_name
    
    extraction_target = dataset_dir / "MontgomerySet"
    if extraction_target.exists():
        print("MontgomerySet already extracted, skipping download and unzip.")
        return
        
    if zip_path.exists():
        zip_path.unlink()
        print(f"Removed partial zip archive {zip_name} to start fresh.")
        
    zip_url = "https://openi.nlm.nih.gov/imgs/collections/NLM-MontgomeryCXRSet.zip"
    
    # Download zip file multithreaded
    zip_path = download_file_multithreaded(zip_url, dataset_dir, zip_name)
    
    # Extract zip file
    print(f"Extracting {zip_name} to {dataset_dir} (this might take a moment)...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dataset_dir)
    print("Extraction complete.")
    
    # Remove the zip to save space
    if zip_path.exists():
        zip_path.unlink()
        print(f"Removed zip archive {zip_name} to save disk space.")

if __name__ == "__main__":
    base_data_dir = Path(os.path.abspath(__file__)).parent.parent.parent / "data"
    download_montgomery(base_data_dir)
    print("Montgomery dataset download and extraction complete.")
