import os
import zipfile

PROJECT_DIR = r"C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis"
ZIP_PATH = r"C:\Users\ACER\BIoinformatics_Training\Rahul_GSE17154_Gastric_Cancer_Portfolio.zip"

# Exclude patterns
EXCLUDE_DIRS = {"__pycache__", ".git", ".pytest_cache", ".venv", "env", "raw_downloads"}
EXCLUDE_EXTS = {".tmp", ".temp", ".pyc", ".pyo"}

print(f"Creating clean portfolio ZIP package at: {ZIP_PATH}...")

total_files = 0
total_size = 0

with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Modify dirs in-place to prune excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in EXCLUDE_EXTS:
                continue
                
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, PROJECT_DIR)
            
            # Avoid putting large raw gz files inside the ZIP
            if "raw_downloads" in rel_path or filename.endswith(".gz") or filename.endswith(".tar"):
                continue
                
            zipf.write(filepath, arcname=os.path.join("Gastric_Cancer_Bioinformatics_GSE17154", rel_path))
            total_files += 1
            total_size += os.path.getsize(filepath)

zip_size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
uncompressed_mb = total_size / (1024 * 1024)

print(f"Successfully created: {ZIP_PATH}")
print(f"Archived {total_files} files.")
print(f"Uncompressed size: {uncompressed_mb:.2f} MB")
print(f"ZIP package size: {zip_size_mb:.2f} MB")
