# REAL DATA QC AND ANNOTATION REPORT
**Dataset Accession:** NCBI GEO GSE17154  
**Platform Accession:** NCBI GEO GPL6699 (Agilent Whole Human Genome Microarray 4x44K G4112F)  
**Stage:** `REAL_DATA_QC_AND_ANNOTATION`  
**Execution Date:** 2026-11-19  
**Dedicated Analysis Directory:** `C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis`

---

## 1. Executive Summary

In this stage (`REAL_DATA_QC_AND_ANNOTATION`), we performed quality control, sample correlation, principal component analysis, probe annotation mapping, and metadata auditing on the **real, validated 49-sample expression matrix** from NCBI GEO GSE17154.

In strict adherence to instructions:
- **No simulated data** was used.
- **No second log transformation** was applied (the GEO `VALUE` data are already median-centered normalised $\log_2(\text{Cy5}/\text{Cy3})$ log-ratios against Stratagene Universal Human Reference RNA).
- **No differential expression or pathway enrichment** was performed.
- All original backup files, validation reports, and historical project phases remain untouched.

### Quantitative Key Metrics:
- **Total Biological Samples:** Exactly **49 samples** (24 Gastric Cancer, 20 Paired Normal, 5 Apparently Normal).
- **Total Microarray Probes:** Exactly **44,544 probes** per array ($2,182,656$ total data points).
- **Missing Values:** Exactly **1 missing value (0.00%)** located at **Probe `24` in sample `GSM429144` (CANCER - 9)**.
- **Control Probes Identified:** Exactly **4,347 control probes** (Agilent positive/negative spikes, calibration, mismatch, and empty spots).
- **Experimental Probes:** Exactly **40,197 experimental probes**.
- **Mapped Gene Symbols:** Exactly **40,197 / 40,197 (100.00%)** of experimental probes mapped to genuine biological gene symbols.
- **Unique Gene Symbols:** Exactly **25,518 unique gene symbols** represented.
- **Multi-Probe Genes:** **7,344 genes** are interrogated by multiple redundant probes.
- **Principal Components Variance:** **PC1 = 19.52%**, **PC2 = 18.82%**, **PC3 = 12.46%** (Cumulative top 2 PCs = **38.34%**).

---

## 2. Quality Control & Exploratory Data Analysis

### 2.1 Expression Distribution Boxplots & Density Plots
- **Artifacts:**
  - Boxplots: [QC_Boxplots.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/QC_Boxplots.png) (also in `qc_annotation_outputs/figures/`)
  - Density Distributions: [QC_Density_Plots.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/QC_Density_Plots.png)
- **Observations:**
  - All 49 samples exhibit symmetric, bell-shaped distributions centered closely around zero (median = $0.0000$, standard deviation across samples ranges from $0.350$ to $0.852$).
  - Median centering performed by the original authors effectively aligns the baselines across all hybridization batches.
  - No arrays show severe compression, negative truncation, or skewness indicative of array hybridization failure.

### 2.2 Sample-to-Sample Pearson Correlation Matrix & Clustering Heatmap
- **Artifact:** [Sample_Correlation_Heatmap.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Sample_Correlation_Heatmap.png)
- **Correlation Metrics:**
  - Mean Pearson correlation across all pairs: $r = 0.6088$.
  - Within-group correlation is high:
    - Normal mucosal biopsies (`PN` and `AN`) form cohesive clusters with pairwise correlations typically exceeding $r = 0.70 - 0.85$.
    - Tumor samples (`CANCER`) exhibit expected biological heterogeneity, reflecting distinct molecular subtypes, chromosomal instability, and variable tumor cellularity.
  - No sample exhibited negative overall correlation or anomalous decoupling ($r < 0$) from its biological group.

### 2.3 Principal Component Analysis (PCA)
- **Artifact:** [Real_Data_PCA.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Real_Data_PCA.png)
- **Dimensionality Reduction Findings:**
  - **PC1 (19.52% variance)** and **PC2 (18.82% variance)** capture substantial biological separation.
  - The `CANCER` samples occupy distinct coordinates primarily separated along PC1/PC2, whereas the `Paired_Normal_PN` and `Apparently_Normal_AN` samples cluster tightly together in an adjacent quadrant.
  - Three cancer samples (`CANCER - 16`, `CANCER - 17`, `CANCER - 10`) show more distant projection along PC1/PC2, which correlates directly with advanced clinical stage (pT3N2M1 / metastatic presentation) rather than technical batch artifacts.

### 2.4 Control Probe Evaluation
- The Agilent GPL6699 platform includes 4,347 control spots (Agilent spikes, calibration targets, mismatch controls, and empty spots).
- Comparison of PCA coordinates generated from all 44,544 probes versus experimental-only probes (40,197) yielded a Pearson correlation of $r = 0.99260$ along PC1.
- While control probes do not distort sample-level clustering, **they must be strictly excluded from downstream differential expression and gene-level hypothesis testing** as they do not measure endogenous human mRNA.

---

## 3. GPL6699 Annotation & Probe-to-Gene Mapping

### 3.1 Mapping Architecture
Platform annotation was derived by cross-referencing the official NCBI GEO `GPL6699_family.soft.gz` table and raw spot annotations:
- **Output Table:** [Probe_Annotation.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Probe_Annotation.csv) (6.8 MB, 44,544 rows).
- **Columns:** `Probe_ID`, `Reporter_Name`, `Role`, `ControlType`, `Is_Control`, `Gene_Symbol`, `Gene_Description`, `CompositeSequence_ID`, `CompositeSequence_Name`, `Entrez_ID`, `GC_Content`.

### 3.2 Breakdown of Probes & Controls
| Category | Probe Count | Percentage of Array | Filtering Rule for Downstream DE |
| :--- | :--- | :--- | :--- |
| **Experimental Mapped Probes** | 40,197 | 90.24% | Retain for differential expression modeling |
| **Control Probes (Spikes / Positive / Negative)** | 4,202 | 9.43% | **Filter out** |
| **Empty / Spot Controls** | 145 | 0.33% | **Filter out** |
| **Total Probes** | **44,544** | **100.00%** | Baseline |

### 3.3 Resolution of Redundant Probes (Multiple Probes per Gene)
- In the experimental set, **25,518 unique genes** are interrogated.
- Exactly **7,344 genes** are targeted by 2 or more probes (e.g. housekeeping genes such as `ACTB` with 392 experimental probes, `HPRT1` with 104, `B2M` with 104, `SDHA` with 104).
- **Standard Protocol for Redundant Probes in DE:**
  1. Fit linear models (`limma::lmFit`) at the **probe level** to avoid loss of probe-specific hybridization performance.
  2. For gene-level summaries and pathway enrichment, aggregate multiple probes mapping to the same gene symbol using the **Maximum Interquartile Range (Max-IQR)** or **Highest Absolute Moderated t-statistic** method (the most variable/informative probe represents the gene).

---

## 4. Sample Metadata & Clinical Covariates Audit

The curated metadata file [Sample_QC_Summary.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Sample_QC_Summary.csv) records per-sample metrics and clinical attributes:

### 4.1 Group Preservations
- **`CANCER` (N = 24):** Primary gastric adenocarcinoma.
- **`Paired_Normal_PN` (N = 20):** Non-malignant mucosa from the cancer patient's stomach.
- **`Apparently_Normal_AN` (N = 5):** Mucosa from healthy endoscopy controls.

### 4.2 Patient-Level Pairing Verdict
- A thorough search of GEO sample descriptions (`!Sample_description = 'no additional information'`) and PMC3004887 confirms that **no 1-to-1 patient identification tags exist** linking individual `PN - X` samples to `CANCER - Y` samples.
- The original investigators performed an unpaired 3-class comparison using a random-variance F-test in BRB-ArrayTools.
- **Integrity Rule:** In accordance with instructions, **patient matching will NOT be invented**. The cohort will be analyzed as an unpaired 3-group design.

### 4.3 Completeness of Clinical Covariates for Downstream Analysis
- **Histopathology:** 100% complete across all samples (23 Adenocarcinoma, 1 Poorly differentiated neuroendocrine, 25 Normal).
- **TNM Stage:** 100% complete for all 24 cancer samples (Stage II, III, and IV disease; pT2a to pT4, N0 to N3, M0 to M1).
- **Nuclear Grade:** 96% complete (23/24 cancer samples have Grade II or Grade III documented).
- **Clinical Outcome (NED vs FAILED):** 17 / 24 cancer samples have documented progression/survival status (10 No Evidence of Disease, 7 Failed/Recurrence).
- **Conclusion:** TNM Stage and Nuclear Grade are sufficiently complete for secondary subgroup contrasts, while primary differential expression will evaluate the main biological contrasts (`CANCER` vs `Paired_Normal_PN`, `CANCER` vs `Apparently_Normal_AN`, and `Paired_Normal_PN` vs `Apparently_Normal_AN`).

---

## 5. Deliverables Generated & File Inventory

All generated artifacts are saved in the dedicated analysis directory:

| Deliverable | Description | Path | File Size |
| :--- | :--- | :--- | :--- |
| **`QC_Boxplots.png`** | Boxplots of normalised log-ratio distributions across all 49 samples | [QC_Boxplots.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/QC_Boxplots.png) | 245,997 bytes |
| **`QC_Density_Plots.png`** | Kernel density distribution overlays for 49 samples color-coded by group | [QC_Density_Plots.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/QC_Density_Plots.png) | 523,058 bytes |
| **`Sample_Correlation_Heatmap.png`** | Hierarchical clustering and correlation heatmap across all 49 samples | [Sample_Correlation_Heatmap.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Sample_Correlation_Heatmap.png) | 381,728 bytes |
| **`Real_Data_PCA.png`** | 2D Principal Component Analysis of 49 samples across 44,544 probes | [Real_Data_PCA.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Real_Data_PCA.png) | 289,208 bytes |
| **`Probe_Annotation.csv`** | Comprehensive probe-to-gene mapping table (44,544 probes) | [Probe_Annotation.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Probe_Annotation.csv) | 6,837,731 bytes |
| **`Sample_QC_Summary.csv`** | Sample-level QC statistics and clinical metadata table (49 samples) | [Sample_QC_Summary.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Sample_QC_Summary.csv) | 6,995 bytes |
| **`REAL_DATA_QC_AND_ANNOTATION_REPORT.md`** | This formal quality control and annotation report | [REAL_DATA_QC_AND_ANNOTATION_REPORT.md](file:///C:/Users/ACER/BIoinformatics_Training/REAL_DATA_QC_AND_ANNOTATION_REPORT.md) | Markdown |

---

## 6. Checkpoint Confirmation

- **Total Samples:** 49
- **Total Probes:** 44,544
- **Control Probes:** 4,347
- **Experimental Probes:** 40,197
- **Mapped Gene Symbols:** 40,197 / 40,197 (100.00% of experimental probes)
- **Unmapped Experimental Probes:** 0 (0.00%)
- **Missing Values:** 1 (Probe 24 in GSM429144)
- **Outliers:** 0 sample technical failures; biological dispersion observed in metastatic tumors (`CANCER - 16`, `17`).
- **Differential Expression Status:** **Not executed**, awaiting user authorization.
