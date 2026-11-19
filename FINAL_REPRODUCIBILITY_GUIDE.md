# FINAL REPRODUCIBILITY GUIDE AND AUDIT LOG

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Workspace:** `C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis`  
**Host Architecture:** Windows 11 (64-bit AMD64) / Python 3.13.14  

---

## 1. System Setup Instructions

### Prerequisites
- Python 3.10+ (tested on Python 3.13.14)
- Git (optional, for repository cloning)

### Dependency Installation
```bash
# Clone the repository
git clone https://github.com/rm0212174-star/Gastric-Cancer-GSE17154.git
cd Gastric-Cancer-GSE17154

# Install verified dependencies
pip install -r requirements.txt
```

---

## 2. Execution Scripts

### Automated One-Click Execution (Windows)
```cmd
cd 12_Real_GSE17154_Analysis
run_pipeline.bat
```

### Automated One-Click Execution (Linux / macOS)
```bash
cd 12_Real_GSE17154_Analysis
bash run_pipeline.sh
```

---

## 3. Step-by-Step Execution Sequence

The automated pipeline executes the following 9 modular steps:
1. `build_probe_annotation.py`: Parses GPL6699 SOFT table and GPR format, filters 4,347 controls, maps 40,197 experimental probes to 25,518 unique genes.
2. `run_qc_and_annotation.py`: Performs missing value imputation (Probe 24 in GSM429144), calculates sample QC, boxplots, density plots, Pearson correlation matrix, and 2D PCA.
3. `run_limma_deg.py`: Fits an unpaired 3-group empirical Bayes linear model (`limma`) across 49 samples, tests 3 biological contrasts, applies BH FDR correction, and generates full DEG tables, volcanos, and heatmaps.
4. `scripts/build_gene_level_degs.py`: Aggregates multi-probe genes using maximum absolute moderated $t$-statistic per unique gene symbol.
5. `scripts/run_enrichment.py`: Queries Enrichr API for GO BP/MF/CC, KEGG 2021, Reactome 2022, and runs fast vectorized ranked GSEA across 25,518 genes.
6. `scripts/run_ppi_network.py`: Queries STRING v12.5 API, constructs NetworkX graph, calculates degree and closeness centrality, renders network visualization.
7. `scripts/run_clinical_analysis.py`: Summarizes TNM stage categories, nuclear differentiation grade, and clinical outcomes for the 24 cancer cases.
8. `scripts/generate_workflow_figure.py`: Renders the high-resolution study workflow schematic diagram (`Study_Workflow_Diagram.png`).
9. `tests/test_pipeline_validation.py`: Executes automated unit test suite asserting data dimensions, FDR bounds, exact DEG counts, and deliverable non-emptiness.

---

## 4. Running Validation Unit Tests

```cmd
python -m unittest -v tests/test_pipeline_validation.py
```

Expected live output:
```
test_01_sample_metadata_counts ... ok
test_02_probe_annotation_and_filtering ... ok
test_03_deg_statistical_validity ... ok
test_04_deg_strict_counts_reproducibility ... ok
test_05_pn_vs_an_no_false_positives ... ok
test_06_required_output_files_exist_and_nonempty ... ok

Ran 6 tests in ~0.3s
OK (Exit Code 0)
```
