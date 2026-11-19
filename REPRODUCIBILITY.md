# REPRODUCIBILITY GUIDE AND EXECUTION PROTOCOL

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  

---

## 1. Prerequisites and Environment Setup

### System Requirements
- Operating System: Windows 10/11, macOS, or Linux (Ubuntu 20.04+)
- Python: Version 3.10 to 3.13 (64-bit)
- RAM: Minimum 8 GB recommended
- Disk Space: ~500 MB free space

### Installation Steps

#### Option A: Pip (Recommended)
```bash
git clone https://github.com/rm0212174-star/Gastric-Cancer-GSE17154.git
cd Gastric-Cancer-GSE17154
pip install -r requirements.txt
```

#### Option B: Conda
```bash
conda env create -f environment.yml
conda activate gastric_cancer_env
```

---

## 2. Automated Pipeline Execution

The complete analytical workflow is packaged into modular scripts that execute sequentially with automated exit-code checking.

### On Windows:
```cmd
cd 12_Real_GSE17154_Analysis
run_pipeline.bat
```

### On Linux / macOS:
```bash
cd 12_Real_GSE17154_Analysis
bash run_pipeline.sh
```

---

## 3. Running the Automated Test Suite

To verify numerical assertions and deliverable integrity independently:
```bash
python -m unittest -v tests/test_pipeline_validation.py
```

Expected output:
```
Ran 6 tests in ~0.3s
OK
```
