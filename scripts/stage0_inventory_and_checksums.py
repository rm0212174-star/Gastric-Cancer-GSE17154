import os
import hashlib
import csv
import datetime

PROJECT_DIR = r"C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis"
BACKUP_DIR = r"C:\Users\ACER\BIoinformatics_Training\01_Original_Backups\12_Real_GSE17154_Analysis_Backup_20261119"

def compute_sha256(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

inventory_rows = []
checksum_rows = []

for root, dirs, files in os.walk(PROJECT_DIR):
    for filename in sorted(files):
        filepath = os.path.join(root, filename)
        rel_path = os.path.relpath(filepath, PROJECT_DIR).replace('\\', '/')
        file_size = os.path.getsize(filepath)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        sha = compute_sha256(filepath)
        
        # Categorize
        ext = os.path.splitext(filename)[1].lower()
        if "raw_downloads" in rel_path or "GSE17154_RAW" in filename or "GPL6699.soft" in filename:
            cat = "Raw_GEO_Download"
        elif "processed" in rel_path or "GSE17154_Expression_Matrix" in filename:
            cat = "Processed_Expression_Matrix"
        elif "metadata" in rel_path or "Metadata" in filename:
            cat = "Metadata"
        elif "annotation" in rel_path or "Annotation" in filename or "GPL6699" in filename:
            cat = "Annotation"
        elif ext == ".py":
            cat = "Python_Script"
        elif ext == ".r":
            cat = "R_Script"
        elif ext == ".bat" or ext == ".sh":
            cat = "Pipeline_Script"
        elif ext == ".csv":
            cat = "Data_or_Result_CSV"
        elif ext in [".png", ".jpg", ".pdf"]:
            cat = "Figure"
        elif ext == ".md" or ext == ".txt":
            cat = "Report_or_Documentation"
        elif ext in [".yml", ".yaml"]:
            cat = "Environment_Config"
        else:
            cat = "Other"
            
        inventory_rows.append({
            "Relative_Path": rel_path,
            "Filename": filename,
            "Category": cat,
            "Size_Bytes": file_size,
            "Last_Modified": mtime,
            "SHA256": sha
        })
        
        checksum_rows.append({
            "Relative_Path": rel_path,
            "SHA256": sha,
            "Size_Bytes": file_size
        })

inv_path = os.path.join(PROJECT_DIR, "PROJECT_FILE_INVENTORY.csv")
with open(inv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Relative_Path", "Filename", "Category", "Size_Bytes", "Last_Modified", "SHA256"])
    writer.writeheader()
    writer.writerows(inventory_rows)

chk_path = os.path.join(PROJECT_DIR, "PROJECT_SHA256_CHECKSUMS.csv")
with open(chk_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Relative_Path", "SHA256", "Size_Bytes"])
    writer.writeheader()
    writer.writerows(checksum_rows)

print(f"Generated {inv_path} with {len(inventory_rows)} files.")
print(f"Generated {chk_path} with {len(checksum_rows)} files.")
