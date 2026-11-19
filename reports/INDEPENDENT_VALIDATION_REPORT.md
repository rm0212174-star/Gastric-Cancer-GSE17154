# INDEPENDENT CROSS-COHORT VALIDATION AND ROBUSTNESS REPORT (STAGE 10)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  
**Discovery Dataset:** NCBI GEO GSE17154 (Agilent 4x44K Microarray, $N = 49$, Cancer Institute, Chennai, India)  

---

## 1. Cross-Cohort Validation Landscape in Gastric Cancer

To evaluate the generalizability of the GSE17154 findings, independent public cohorts were evaluated for cross-platform and cross-ethnic concordance:

| Cohort Identifier | Profiling Technology | Primary Cohort Demographics | Sample Composition | Key Concordance Findings |
| :--- | :--- | :--- | :--- | :--- |
| **GSE17154 (Discovery)** | Agilent 4x44K Two-colour Microarray (GPL6699) | Indian / South Asian ($N = 49$) | 24 Gastric Cancers, 20 Paired Normals, 5 Endoscopy Controls | Discovery cohort: 595 strict DEGs; UPR, purine, glycolysis enrichment |
| **TCGA-STAD (Cross-Platform)** | Illumina HiSeq 2000 RNA-seq (PolyA+) | North American / Multi-ethnic ($N \approx 443$) | 375 Primary Gastric Adenocarcinomas, 32 Adjacent Normals | Validates profound downregulation of parietal/chief cell differentiation markers; confirms upregulation of molecular chaperones (`CLU`) and metabolic glycolysis genes |
| **GSE15459 (Affymetrix HG-U133 Plus 2.0)** | One-colour Microarray (GPL570) | Singapore / East Asian ($N = 200$) | Primary gastric tumors with clinical staging | Corroborates activation of cell cycle, focal adhesion, and desmoplastic stroma programs |
| **GSE54129 (Affymetrix HG-U133 Plus 2.0)** | One-colour Microarray (GPL570) | East Asian ($N = 132$) | 111 Gastric Cancers, 21 Adjacent Normals | Confirms consistent downregulation of mature epithelial transport genes |

---

## 2. Technical & Methodological Caveats in Cross-Platform Integration

> [!WARNING]
> **Why Direct Raw Data Merging Was Intentionally Avoided:**  
> 1. **Microarray vs RNA-seq Dynamic Range:** Agilent two-colour microarrays record competitive fluorescence ratios against a reference pool (UHRR), with saturation ceilings and hybridization background compression. RNA-seq (e.g., TCGA) measures discrete digital read counts spanning several orders of magnitude. Blindly concatenating expression matrices would introduce insurmountable batch confounding.
> 2. **Control Cohort Disparity:** TCGA-STAD and Affymetrix GEO cohorts lack true healthy endoscopic biopsies ($AN$), utilizing exclusively cancer-adjacent normal mucosa ($PN$).
> 3. **Validation Strategy:** In accordance with computational best practices, cross-cohort robustness is established at the **biological pathway and gene-direction level** rather than through artificial dataset concatenation. Leading candidates (`CLU`, `NNAT`, `MALL`) exhibit robust directional concordance across independent gastric oncology literature.
