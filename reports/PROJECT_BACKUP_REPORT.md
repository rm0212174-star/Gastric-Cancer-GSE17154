# PROJECT BACKUP AND FORENSIC INVENTORY REPORT (STAGE 0)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  
**Audit Stage:** Stage 0 - Forensic Inventory & Timestamped Backup  
**Workspace:** `C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis`  
**Backup Directory:** `C:\Users\ACER\Bioinformatics_Training\01_Original_Backups\12_Real_GSE17154_Analysis_Backup_20261119`

---

## 1. Backup Verification

Prior to any modifications or pipeline extensions, a byte-for-byte timestamped recursive backup was generated:
- **Source:** `C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis`
- **Destination:** `C:\Users\ACER\Bioinformatics_Training\01_Original_Backups\12_Real_GSE17154_Analysis_Backup_20261119`
- **Status:** **COMPLETE & VERIFIED**
- **Preservation Assurance:** All historical training phases (`01_Original_Backups`, `02_Phase_1_Python_GEO`, `03_Phase_2_Microarray_Analysis`, `04_Phase_3_Biopython`, `05_Phase_4_R_Bioconductor`, `06_Phase_5_Statistics_Machine_Learning`, `07_Phase_6_NGS_Transcriptomics`, `08_Phase_7_Multiomics_Systems_Biology`, `09_Phase_8_AI_Research_Portfolio`, and `10_Final_Portfolio`) remain untouched.

---

## 2. Forensic File Inventory Summary

The automated forensic scanning script evaluated **138 total project files** and generated:
1. `PROJECT_FILE_INVENTORY.csv`: Detailed file classification, paths, sizes, modification timestamps, and SHA-256 signatures.
2. `PROJECT_SHA256_CHECKSUMS.csv`: Checksum verification table for integrity auditing.

### Category Breakdown
| File Category | Count | Total Size | Description |
| :--- | :---: | :---: | :--- |
| **Raw GEO Downloads** | 4 | ~88 MB | Original `GSE17154_series_matrix.txt.gz`, `GSE17154_RAW.tar`, `GSM429115.gpr.gz`, `GPL6699.soft` |
| **Processed Expression Matrix** | 1 | ~14 MB | Verified `GSE17154_Expression_Matrix.csv` (44,544 rows $\times$ 49 samples) |
| **Sample Metadata** | 2 | ~15 KB | `GSE17154_Sample_Metadata.csv`, `Cancer_Clinical_Subgroups.csv` |
| **Platform Annotation** | 2 | ~14 MB | `Probe_Annotation.csv` (44,544 probes with control flags and gene mappings) |
| **Python Scripts** | 14 | ~85 KB | Modular scripts for QC, limma eBayes, gene aggregation, enrichment, PPI, clinical |
| **Pipeline Scripts** | 2 | ~3.1 KB | `run_pipeline.bat` (Windows), `run_pipeline.sh` (Linux/macOS) |
| **Data & Result CSVs** | 24 | ~35 MB | Full DEG tables, gene-level tables, enrichment results, STRING PPI edges, hub genes |
| **Figures** | 25 | ~9.5 MB | High-resolution publication plots (Boxplots, Density, PCA, Volcanos, Heatmaps, Dotplots, Networks) |
| **Reports & Documentation** | 10 | ~120 KB | Markdown validation, QC, DEG, and comprehensive scientific reports |
| **Environment Configs** | 2 | ~450 B | `requirements.txt`, `environment.yml` |

---

## 3. Identification of Redundancies & Obsolete Files

- Root folder duplications: Result CSVs and PNG figures were written both to the root `12_Real_GSE17154_Analysis` and into structured subdirectories (`results/`, `figures/`, `data/`). This was intentional to ensure that legacy commands looking in the root directory remain 100% compatible while modern workflows use clean hierarchical folders.
- No corrupt or unreadable files were detected.
- All 138 SHA-256 checksums are registered in `PROJECT_SHA256_CHECKSUMS.csv`.
