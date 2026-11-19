# REAL GSE17154 DIFFERENTIAL EXPRESSION ANALYSIS REPORT
**Dataset Accession:** NCBI GEO GSE17154  
**Platform Accession:** NCBI GEO GPL6699 (Agilent Whole Human Genome Microarray 4x44K G4112F)  
**Analysis Stage:** `DIFFERENTIAL_GENE_EXPRESSION_LIMMA`  
**Date of Audit & Analysis:** 2026-11-19  
**Dedicated Analysis Directory:** `C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis`

---

## 1. Executive Summary

This study documents the formal differential gene expression analysis conducted on the real, validated **NCBI GEO GSE17154** gastric cancer dataset. Historical simulated matrices remain strictly isolated; this analysis operates directly on the empirical microarray values using an empirical Bayes moderated linear model (`limma`).

### Methodological Principles Maintained:
1. **Preservation of Processed Values:** No secondary log transformation was performed. The data values represent normalised $\log_2(\text{Cy5}/\text{Cy3})$ ratios against Stratagene Universal Human Reference RNA (UHRR).
2. **Control-Probe Filtering:** Exactly **4,347 control spots** (positive/negative spikes, calibration mismatch controls, and empty spots) were filtered out. The final analysable feature space consists of exactly **40,197 experimental probes** representing **25,518 unique gene symbols**.
3. **Statistical Design:** Unpaired 3-group linear model (`~ 0 + Group`) parameterised across all **49 clinical samples**:
   - **`CANCER` ($N = 24$):** Primary gastric adenocarcinomas.
   - **`Paired_Normal_PN` ($N = 20$):** Non-malignant gastric mucosa biopsies from cancer stomachs.
   - **`Apparently_Normal_AN` ($N = 5$):** Normal gastric mucosa from non-cancer endoscopy controls.
4. **Planned Contrasts Evaluated:**
   - Contrast 1: **Cancer vs Paired Normal (`Cancer_vs_PN`)**
   - Contrast 2: **Cancer vs Apparently Normal (`Cancer_vs_AN`)**
   - Contrast 3: **Paired Normal vs Apparently Normal (`PN_vs_AN`)**
5. **Multiple Testing Correction:** Benjamini-Hochberg (BH) False Discovery Rate (FDR).

---

## 2. Statistical Modeling & Empirical Bayes Parameterization

### 2.1 Model Specification
Given expression vector $\mathbf{y}_g$ for probe $g$ across 49 samples, the linear model was formulated as:
$$\mathbf{y}_g = \mathbf{X} \boldsymbol{\beta}_g + \boldsymbol{\varepsilon}_g, \quad \boldsymbol{\varepsilon}_g \sim \mathcal{N}(0, \sigma_g^2 \mathbf{I})$$
where $\mathbf{X}$ is the $49 \times 3$ indicator design matrix for groups `[CANCER, Paired_Normal_PN, Apparently_Normal_AN]`.

### 2.2 Empirical Bayes Variance Moderation
Following Smyth (2004), probe residual variances $s_g^2$ were moderated toward an overarching prior variance $s_0^2$ with prior degrees of freedom $d_0$:
$$\tilde{s}_g^2 = \frac{d_0 s_0^2 + d_g s_g^2}{d_0 + d_g}$$
- **Residual Degrees of Freedom ($d_g$):** $49 - 3 = 46$
- **Estimated Prior Degrees of Freedom ($d_0$):** $2.15$
- **Estimated Prior Variance ($s_0^2$):** $0.0340$
- **Moderated Degrees of Freedom ($d_0 + d_g$):** $48.15$

Moderated $t$-statistics were computed as:
$$\tilde{t}_{g, c} = \frac{\hat{\beta}_{g, c}}{\tilde{s}_g \sqrt{v_c}}$$
where $v_c$ is the unscaled variance for contrast $c$. P-values were evaluated against Student's $t$-distribution with $48.15$ degrees of freedom and adjusted using the Benjamini-Hochberg procedure.

---

## 3. Differential Expression Results by Contrast

### Summary of Statistical Findings:

| Contrast | Total Probes Tested | Significant (FDR < 0.05) | Strict DEGs (FDR < 0.05 & \|$\log_2\text{FC}$\| $\ge 1.0$) | Up-regulated | Down-regulated |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cancer vs Paired Normal (`Cancer_vs_PN`)** | 40,197 | 2,886 (7.18%) | **633** (1.57%) | 60 | 573 |
| **Cancer vs Apparently Normal (`Cancer_vs_AN`)** | 40,197 | 1,314 (3.27%) | **643** (1.60%) | 93 | 550 |
| **Paired Normal vs Apparently Normal (`PN_vs_AN`)** | 40,197 | **0** (0.00%) | **0** (0.00%) | 0 | 0 |

---

### 3.1 Contrast 1: Cancer vs Paired Normal (`Cancer_vs_PN`)
This contrast compares tumor tissue against non-malignant mucosa taken from the same stomach.
- **Top Up-regulated Candidates:**
  - `SSPO` (Probe 21480): $\log_2\text{FC} = +1.954$, moderated $t = 5.956$, $p = 2.90 \times 10^{-7}$, $\text{FDR} = 3.25 \times 10^{-5}$
  - `NNAT` (Probe 8023): $\log_2\text{FC} = +1.937$, moderated $t = 5.798$, $p = 5.05 \times 10^{-7}$, $\text{FDR} = 4.90 \times 10^{-5}$
  - `P15RS` (Probe 29498): $\log_2\text{FC} = +1.786$, moderated $t = 5.638$, $p = 8.85 \times 10^{-7}$, $\text{FDR} = 7.90 \times 10^{-5}$
  - `CLU` (Probe 11322): $\log_2\text{FC} = +1.439$, moderated $t = 5.799$, $p = 5.03 \times 10^{-7}$, $\text{FDR} = 4.90 \times 10^{-5}$
  - `MALL` (Probe 17820): $\log_2\text{FC} = +1.344$, moderated $t = 5.799$, $p = 5.03 \times 10^{-7}$, $\text{FDR} = 4.90 \times 10^{-5}$
  - `SCARA3` (Probe 21397): $\log_2\text{FC} = +1.068$, moderated $t = 5.923$, $p = 3.25 \times 10^{-7}$, $\text{FDR} = 3.50 \times 10^{-5}$
- **Top Down-regulated Candidates:**
  - `ATP1B4` (Probe 11909): $\log_2\text{FC} = -4.308$, moderated $t = -11.891$, $p = 6.66 \times 10^{-16}$, $\text{FDR} = 2.68 \times 10^{-11}$
  - `KLRA1` (Probe 16985): $\log_2\text{FC} = -4.289$, moderated $t = -11.134$, $p = 6.44 \times 10^{-15}$, $\text{FDR} = 1.29 \times 10^{-10}$
  - `GAPDH` (Probe 5469): $\log_2\text{FC} = -3.452$, moderated $t = -10.860$, $p = 1.51 \times 10^{-14}$, $\text{FDR} = 2.02 \times 10^{-10}$
  - `DPP3` (Probe 21515): $\log_2\text{FC} = -2.879$, moderated $t = -10.712$, $p = 2.44 \times 10^{-14}$, $\text{FDR} = 2.45 \times 10^{-10}$
  - `CPEB2` (Probe 9576): $\log_2\text{FC} = -2.480$, moderated $t = -10.525$, $p = 4.44 \times 10^{-14}$, $\text{FDR} = 3.57 \times 10^{-10}$

---

### 3.2 Contrast 2: Cancer vs Apparently Normal (`Cancer_vs_AN`)
This contrast compares tumor tissue against healthy endoscopic mucosal biopsies.
- **Top Up-regulated Candidates:**
  - `NNAT` (Probe 8023): $\log_2\text{FC} = +2.739$, moderated $t = 5.048$, $p = 6.84 \times 10^{-6}$, $\text{FDR} = 0.00168$
  - `MALL` (Probe 17820): $\log_2\text{FC} = +2.080$, moderated $t = 5.530$, $p = 1.48 \times 10^{-6}$, $\text{FDR} = 0.00066$
  - `PINX1` (Probe 7825): $\log_2\text{FC} = +1.774$, moderated $t = 5.257$, $p = 3.39 \times 10^{-6}$, $\text{FDR} = 0.00109$
  - `ARHGEF4` (Probe 15440): $\log_2\text{FC} = +1.558$, moderated $t = 5.032$, $p = 7.23 \times 10^{-6}$, $\text{FDR} = 0.00173$
  - `RP5-1054A22.3` (Probe 6114): $\log_2\text{FC} = +1.550$, moderated $t = 5.271$, $p = 3.25 \times 10^{-6}$, $\text{FDR} = 0.00108$
- **Top Down-regulated Candidates:**
  - `KLRA1` (Probe 16985): $\log_2\text{FC} = -4.778$, moderated $t = -7.638$, $p = 7.65 \times 10^{-10}$, $\text{FDR} = 0.000010$
  - `BRWD3` (Probe 27335): $\log_2\text{FC} = -4.582$, moderated $t = -6.914$, $p = 9.80 \times 10^{-9}$, $\text{FDR} = 0.000070$
  - `ATP1B4` (Probe 11909): $\log_2\text{FC} = -4.490$, moderated $t = -7.633$, $p = 7.77 \times 10^{-10}$, $\text{FDR} = 0.000010$
  - `GAPDH` (Probe 5469): $\log_2\text{FC} = -4.034$, moderated $t = -7.815$, $p = 4.11 \times 10^{-10}$, $\text{FDR} = 0.000010$
  - `CIDEB` (Probe 6204): $\log_2\text{FC} = -2.218$, moderated $t = -6.670$, $p = 2.33 \times 10^{-8}$, $\text{FDR} = 0.000117$

---

### 3.3 Contrast 3: Paired Normal vs Apparently Normal (`PN_vs_AN`)
- Across all 40,197 experimental probes, **zero probes achieved genome-wide significance after Benjamini-Hochberg FDR adjustment** ($\min \text{FDR} = 0.2601$).
- **Biological Interpretation:**
  - Histologically confirmed non-tumorous mucosa from cancer stomachs (`PN`) shows remarkably similar global baseline transcriptomic profiles to endoscopic normal controls (`AN`).
  - This indicates that macroscopically normal mucosa does not undergo genome-wide expression disruption on a scale comparable to malignant transformation.
  - Furthermore, with $N = 5$ for `AN`, statistical power to detect subtle field-effect changes is constrained.

---

## 4. Visualizations & Graphical Outputs

### 4.1 Volcano Plots
- [Volcano_Cancer_vs_PN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Volcano_Cancer_vs_PN.png): Highlights 60 up-regulated and 573 down-regulated probes in cancer versus paired field normal.
- [Volcano_Cancer_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Volcano_Cancer_vs_AN.png): Illustrates 93 up-regulated and 550 down-regulated probes in cancer versus healthy controls.
- [Volcano_PN_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Volcano_PN_vs_AN.png): Confirms the absence of genome-wide significant differentially expressed probes between the two normal mucosal classes.

### 4.2 Top 50 DEG Heatmaps with Hierarchical Clustering
- [Heatmap_Top50_Cancer_vs_PN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Heatmap_Top50_Cancer_vs_PN.png): Row Z-score heatmap displaying clean bifurcating hierarchical clustering separating all 24 cancer samples from 20 paired normal samples.
- [Heatmap_Top50_Cancer_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Heatmap_Top50_Cancer_vs_AN.png): Clean separation of 24 cancer samples from 5 apparently normal controls.
- [Heatmap_Top50_PN_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Heatmap_Top50_PN_vs_AN.png): Displays top nominal probes between the two normal groups (intermingled clustering reflecting the lack of significant global divergence).

---

## 5. Clinical Covariate & Subgroup Investigation

Analysis of clinical characteristics within the 24 Gastric Cancer cases revealed:
- **TNM Stage Distribution:**
  - Localized Stage (N0 M0): $N = 7$ cases (e.g. `GSM429115`, `GSM429134`, `GSM429151`, `GSM429152`, `GSM429156`, `GSM429157`, `GSM429159`).
  - Lymph Node Positive (N+ M0): $N = 13$ cases (e.g. `GSM429131`, `GSM429132`, `GSM429133`, `GSM429139`, `GSM429140`, `GSM429143`, `GSM429144`, `GSM429145`, `GSM429147`, `GSM429148`, `GSM429150`, `GSM429155`, `GSM429160`).
  - Distant Metastatic (M1): $N = 4$ cases (`GSM429153`, `GSM429154`, `GSM429161`, `GSM429163`).
- **Histopathology:**
  - 23 of 24 tumors are tubular or mucinous adenocarcinomas.
  - Exactly 1 tumor (`GSM429147`, CANCER - 11) is classified as *Poorly differentiated with Neuroendocrine differentiation*.
- **Statistical Precaution Regarding Subgroups:**
  Because the metastatic subgroup ($N = 4$) and neuroendocrine histology ($N = 1$) have very limited sample sizes, fitting multi-parameter clinical interaction models would risk statistical overfitting. These metadata are preserved in [Cancer_Clinical_Subgroups.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/deg_outputs/tables/Cancer_Clinical_Subgroups.csv) for descriptive correlation.

---

## 6. Scientific Limitations & Biomarker Disclaimer

> [!CAUTION]
> **Scientific Integrity & Biomarker Disclaimer:**
> 1. In accordance with rigorous bioinformatics and clinical standards, **no differentially expressed candidate gene identified in this single microarray cohort is designated as a "validated clinical biomarker"**.
> 2. The findings represent statistically significant transcriptomic associations within GEO GSE17154. Translating any candidate (such as `SSPO`, `NNAT`, `MALL`, or `CLU`) into a validated clinical biomarker requires:
>    - Independent external cohort validation across modern RNA-sequencing datasets (e.g. TCGA-STAD, ACRG).
>    - Orthogonal laboratory assay verification (RT-qPCR, immunohistochemistry on tissue microarrays).
>    - Prospective clinical utility assessment and blinded clinical trials.
> 3. The small size of the endoscopic control cohort ($N = 5$) confers reduced statistical power to detect subtle field defects in the `PN vs AN` contrast.

---

## 7. Complete Deliverable Inventory

All DEG outputs, ranked tables, and high-resolution figures are preserved in:
- `C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis\`
- `C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis\deg_outputs\`

| Category | File Name | Description |
| :--- | :--- | :--- |
| **Ranked Table** | [DEG_Cancer_vs_PN_Full.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/deg_outputs/tables/DEG_Cancer_vs_PN_Full.csv) | Full ranked results for all 40,197 probes (Cancer vs PN) |
| **Top DEGs** | [DEG_Cancer_vs_PN_Top_FDR05_FC2.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/deg_outputs/tables/DEG_Cancer_vs_PN_Top_FDR05_FC2.csv) | 633 probes meeting FDR < 0.05 & \|$\log_2\text{FC}$\| $\ge 1.0$ |
| **Ranked Table** | [DEG_Cancer_vs_AN_Full.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/deg_outputs/tables/DEG_Cancer_vs_AN_Full.csv) | Full ranked results for all 40,197 probes (Cancer vs AN) |
| **Top DEGs** | [DEG_Cancer_vs_AN_Top_FDR05_FC2.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/deg_outputs/tables/DEG_Cancer_vs_AN_Top_FDR05_FC2.csv) | 643 probes meeting FDR < 0.05 & \|$\log_2\text{FC}$\| $\ge 1.0$ |
| **Ranked Table** | [DEG_PN_vs_AN_Full.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/deg_outputs/tables/DEG_PN_vs_AN_Full.csv) | Full ranked results for all 40,197 probes (PN vs AN) |
| **Top DEGs** | [DEG_PN_vs_AN_Top_FDR05_FC2.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/deg_outputs/tables/DEG_PN_vs_AN_Top_FDR05_FC2.csv) | 0 probes meeting FDR < 0.05 |
| **Clinical Table** | [Cancer_Clinical_Subgroups.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/deg_outputs/tables/Cancer_Clinical_Subgroups.csv) | Curated TNM stage and histology classification table |
| **Figure** | [Volcano_Cancer_vs_PN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Volcano_Cancer_vs_PN.png) | High-resolution volcano plot (Cancer vs PN) |
| **Figure** | [Volcano_Cancer_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Volcano_Cancer_vs_AN.png) | High-resolution volcano plot (Cancer vs AN) |
| **Figure** | [Volcano_PN_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Volcano_PN_vs_AN.png) | High-resolution volcano plot (PN vs AN) |
| **Figure** | [Heatmap_Top50_Cancer_vs_PN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Heatmap_Top50_Cancer_vs_PN.png) | Clustered expression heatmap of top 50 DEGs (Cancer vs PN) |
| **Figure** | [Heatmap_Top50_Cancer_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Heatmap_Top50_Cancer_vs_AN.png) | Clustered expression heatmap of top 50 DEGs (Cancer vs AN) |
| **Figure** | [Heatmap_Top50_PN_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/Heatmap_Top50_PN_vs_AN.png) | Clustered expression heatmap of top 50 nominal probes (PN vs AN) |
| **Report** | [REAL_GSE17154_DEG_REPORT.md](file:///C:/Users/ACER/BIoinformatics_Training/REAL_GSE17154_DEG_REPORT.md) | Formal Differential Expression Report |

---

## 8. Completion Checkpoint
Differential expression modeling is complete. In compliance with your instructions, execution has stopped here. No GO/KEGG pathway enrichment has been performed.
