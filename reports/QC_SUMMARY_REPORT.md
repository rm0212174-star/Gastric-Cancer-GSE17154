# QUALITY CONTROL & EXPLORATORY DATA ANALYSIS REPORT (STAGE 4)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  
**Cohort Accession:** GSE17154 | **Platform:** GPL6699 (44,544 probes $\times$ 49 samples)  

---

## 1. Missing-Value Inspection
- **Total Data Points Tested:** $44,544 \times 49 = 2,182,656$
- **Total Missing Entries:** Exactly **1** missing value (0.000046% of dataset).
- **Location:** Sample `GSM429144` (`CANCER - 9 (gastric cancer study)`), Probe ID `24`.
- **Resolution Strategy:** Imputed using the across-sample mean for Probe 24 ($\mu = -0.0497$). No sample or probe required exclusion due to missingness.

---

## 2. Expression Distribution & Quality Metrics
- **Array Value Scale:** Processed $\log_2(\text{Cy5}/\text{Cy3})$ normalized ratios against Stratagene Universal Human Reference RNA (UHRR).
- **Global Distribution:** Median = `0.0000`, Mean = `0.0826`, Min = `-6.0797`, Max = `+8.3823`, Std = `0.5676`.
- **Boxplots:** [QC_Boxplots.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/QC_Boxplots.png) demonstrates uniform median-centering across all 49 arrays with well-balanced interquartile ranges (IQR).
- **Density Distributions:** [QC_Density_Plots.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/QC_Density_Plots.png) shows smooth Gaussian-like empirical kernel density curves without bi-modal dye artifacts.

---

## 3. Sample-to-Sample Correlation & Hierarchical Clustering
- **Pearson Correlation Matrix:** [Sample_Correlation_Heatmap.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Sample_Correlation_Heatmap.png)
  - Minimum Correlation: $r = 0.0034$ (between divergent metastatic tumor `CANCER - 17` and normal mucosal controls)
  - Mean Pairwise Correlation: $r = 0.6088$
  - Normal mucosal samples (`PN` and `AN`) exhibit tight internal concordance ($r > 0.75$).
- **Hierarchical Clustering:** [Sample_Clustering.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Sample_Clustering.png)
  - Dendrogram (Average Linkage, $1 - r$ distance) cleanly segregates the non-malignant mucosa (`PN` and `AN`) into cohesive normal clusters, while primary gastric cancer specimens cluster into biological sub-branches reflecting clinical heterogeneity.

---

## 4. Principal Component Analysis (PCA) & Outlier Audit
- **PCA Dimensionality Reduction:** [Real_Data_PCA.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Real_Data_PCA.png)
  - **PC1 (19.52% of total variance):** Dominant biological axis separating gastric adenocarcinoma from non-tumorous mucosa.
  - **PC2 (18.82% of total variance):** Captures tumor-intrinsic transcriptional divergence. Advanced metastatic cases (`CANCER - 16`, `CANCER - 17`) project to the extreme periphery of PC1/PC2 space, reflecting biological tumor progression rather than technical assay failure.
  - **Decision:** In accordance with user guidelines, **no samples were arbitrarily discarded**. All 49 samples passed quality control.
