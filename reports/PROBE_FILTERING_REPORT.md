# PROBE FILTERING & PLATFORM ANNOTATION AUDIT REPORT (STAGE 3)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  
**Platform Accession:** GPL6699 (Agilent Whole Human Genome Microarray 4x44K G4112F)  

---

## 1. Feature Dimension Reconciliation

| Platform Characteristic | Count | Percentage | Filtering Action |
| :--- | :---: | :---: | :--- |
| **Total Features on Array** | **44,544** | 100.00% | Verified against official GPL6699 SOFT file |
| **Technical Control Spots** | **4,347** | 9.76% | **FILTERED OUT** prior to differential expression |
| **Analysable Experimental Probes** | **40,197** | 90.24% | **RETAINED** for empirical Bayes modeling |
| **Unique Human Gene Symbols** | **25,518** | — | Unique mapped biological transcripts |

---

## 2. Objective Filtering Rules Applied

1. **Negative & Non-specific Hybridization Controls:** Identified by `ControlType = "negative"` or Agilent control prefixes (`NC1_*`, `NC2_*`, `NegativeControl_*`).
2. **Structural & Engineering Spots:** Spatial grid markers, corner calibration probes (`BrightCorner`), and non-human spike-ins.
3. **Validation Proof:** Principal Component Analysis on experimental probes alone vs all 44,544 probes demonstrated an identical coordinate structure ($r = 0.9926$), confirming that control spots do not introduce artificial batch effects, but must be removed to avoid statistical artifacts in differential testing.

---

## 3. Gene-Level Aggregation Methodology

- **Multi-Probe Redundancy:** 7,344 unique genes possess $>1$ probe on the array (e.g., `ACTB` is interrogated by 392 separate spots).
- **Strategy:** Maximum absolute moderated $t$-statistic per gene:
  $$\text{Selected Probe}_g = \arg\max_{p \in \text{Probes}(g)} |t_p|$$
- **Statistical Justification:** This approach selects the hybridization spot with the highest signal-to-noise ratio and statistical power for each unique transcript, avoiding multiple-testing dilution and false independence assumptions.
