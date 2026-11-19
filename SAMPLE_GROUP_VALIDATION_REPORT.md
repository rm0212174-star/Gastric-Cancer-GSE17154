# SAMPLE GROUP VALIDATION REPORT (STAGE 2)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  
**Cohort Accession:** NCBI GEO GSE17154  
**Total Clinical Specimens:** 49  

---

## 1. Group Breakdown & Biological Definition

| Cohort Identifier | Sample Count ($N$) | Biological Source & Clinical Definition | Histopathology | Statistical Role |
| :--- | :---: | :--- | :--- | :--- |
| **`CANCER`** | 24 | Primary gastric tumor surgical biopsies | Adenocarcinoma ($N=23$), Neuroendocrine ($N=1$) | Disease Test Group |
| **`Paired_Normal_PN`** | 20 | Non-malignant gastric mucosal biopsies from the **same stomach** as cancer patients, sampled $>5$ cm remote from the lesion margin | Histologically verified non-tumorous mucosa | Paired-Source Reference (Analyzed Unpaired) |
| **`Apparently_Normal_AN`** | 5 | Endoscopic gastric mucosal biopsies from healthy volunteer controls with no evidence of malignancy | Endoscopically normal mucosa | True Healthy Control Reference |

---

## 2. Statistical Pairing vs Tissue Origin Disambiguation

> [!IMPORTANT]
> **Biostatistical Requirement: Unpaired Modeling**  
> 1. In the public GEO record `GSE17154`, the sample titles are anonymous (`CANCER - 1`, `PN - 1`, etc.), and the series description states `!Sample_description = "no additional information"`.
> 2. The sample sizes are asymmetrical ($N_{\text{Cancer}} = 24$, $N_{\text{PN}} = 20$). No deterministic 1-to-1 linkage exists between specific cancer and normal samples in public records.
> 3. Imposing a paired $t$-test or blocked multi-level model (`~ Patient + Tissue`) would require arbitrarily fabricating patient pairings.
> 4. In full agreement with the original investigators (Rajkumar et al., 2010), who utilized an unpaired random-variance $F$-test in BRB-ArrayTools, all differential expression analyses in this project strictly enforce an **unpaired 3-group design** (`~ 0 + Group`).
> 5. The term `Paired_Normal_PN` is retained exclusively to denote biological anatomical provenance (same-stomach mucosa), not statistical dependency.

---

## 3. Recommended Comparison Contrasts
- **Contrast A (`Cancer_vs_PN`):** Cancer vs non-tumorous mucosa from cancer patients ($24 \text{ vs } 20$).
- **Contrast B (`Cancer_vs_AN`):** Cancer vs apparently normal endoscopic controls ($24 \text{ vs } 5$).
- **Contrast C (`PN_vs_AN`):** Non-tumorous mucosa from cancer patients vs healthy endoscopic controls ($20 \text{ vs } 5$).
