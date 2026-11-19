# FINAL PROJECT SUMMARY: GSE17154 GASTRIC CANCER TRANSCRIPTOMICS

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date of Release:** 2026-11-19  
**Platform:** Agilent GPL6699 (Whole Human Genome Microarray 4x44K)  
**Dataset:** NCBI GEO GSE17154 (49 clinical samples)  
**Author / Investigator:** MSc Biotechnology Candidate / Bioinformatics Analyst  
**Release Status:** **`VERIFIED WITH DOCUMENTED LIMITATIONS`**

---

## 1. Executive Scientific Overview

This project provides an audited, end-to-end reproducible computational biology analysis of primary gastric adenocarcinoma using real microarray transcriptomics from NCBI GEO dataset GSE17154.

Prior analyses in early training stages relied on simulated matrices and incorrectly assumed patient-level pairing. This release independently audits the empirical GEO dataset, proves that patient-matching identifiers do not exist in the public record, and implements a mathematically sound **unpaired 3-group empirical Bayes linear model** (`limma`).

---

## 2. Quantitative Summary of Key Findings

1. **Cohort Breakdown:** 24 Gastric Cancers (`CANCER`), 20 Paired Normal mucosal biopsies from cancer stomachs (`Paired_Normal_PN`), and 5 Healthy Endoscopy Controls (`Apparently_Normal_AN`). Total: 49 samples.
2. **Feature Space:** 44,544 total hybridization spots $\rightarrow$ 4,347 control spots filtered $\rightarrow$ 40,197 experimental probes analyzed $\rightarrow$ 25,518 unique mapped human genes.
3. **Differential Expression:**
   - **Cancer vs Paired Normal:** 633 strict probes ($|\log_2\text{FC}| \ge 1.0$, $\text{FDR} < 0.05$), summarizing to **595 strict unique genes** (52 Up, 543 Down). Top upregulated: `SSPO` (+1.95), `NNAT` (+1.94), `P15RS` (+1.79), `CLU` (+1.44), `MALL` (+1.34). Top downregulated: `ATP1B4` (-4.31), `KLRA1` (-4.29).
   - **Cancer vs Apparently Normal:** 643 strict probes, summarizing to **605 strict unique genes** (81 Up, 524 Down).
   - **Paired Normal vs Apparently Normal:** **0 DEGs** ($\text{min FDR} = 0.2601$), reflecting that field normal mucosa preserves baseline transcriptomic integrity, though statistical power is constrained by $N = 5$ in controls.
4. **Coordinated Pathways (Ranked GSEA across 25,518 genes):** Purine metabolism ($p_{\text{adj}} = 3.52 \times 10^{-11}$), Unfolded Protein Response ($p_{\text{adj}} = 2.09 \times 10^{-8}$), Glycolysis/Gluconeogenesis ($p_{\text{adj}} = 6.18 \times 10^{-8}$), and JAK-STAT signaling ($p_{\text{adj}} = 4.09 \times 10^{-7}$).
5. **STRING Interactome Hubs:** `GAPDH` (deg 5), `ACTB` (deg 5), `CSF3` (deg 3), `LTF` (deg 3), and `CTSD` (deg 2). All hubs are reported as computational hypotheses, not proven biomarkers.
6. **Reproducibility:** 9-step automated pipeline (`run_pipeline.bat` / `.sh`) and 6-test automated validation suite with 100% pass rate.
