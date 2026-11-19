# SCIENTIFIC RESULTS SUMMARY

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  

---

## 1. Quality Control & Dimensionality Reduction

- **Global Expression:** Median = `0.0000`, Mean = `0.0826`, Min = `-6.0797`, Max = `+8.3823`, Std = `0.5676`.
- **Sample Correlation:** Mean pairwise Pearson correlation $r = 0.6088$. Normal mucosa samples (`PN` and `AN`) showed strong internal concordance ($r > 0.75$).
- **Principal Component Analysis:** PC1 accounted for **19.52%** and PC2 accounted for **18.82%** of total variance, achieving clear separation between malignant tumors and normal mucosa. Advanced metastatic tumors (`CANCER - 16`, `CANCER - 17`) projected furthest along PC1.

---

## 2. Differential Gene Expression Landscape

### Probe-Level vs Gene-Level Results
| Contrast | Feature Level | Total Tested | FDR < 0.05 | Strict DEGs (FDR < 0.05 & \|Log2FC\| $\ge$ 1.0) | Up-regulated | Down-regulated |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Cancer vs PN** | **Probe-Level** | 40,197 | 2,886 (7.18%) | **633** (1.57%) | 60 | 573 |
| | **Gene-Level** | 25,518 | 2,625 (10.29%) | **595** (2.33%) | 52 | 543 |
| **Cancer vs AN** | **Probe-Level** | 40,197 | 1,314 (3.27%) | **643** (1.60%) | 93 | 550 |
| | **Gene-Level** | 25,518 | 1,232 (4.83%) | **605** (2.37%) | 81 | 524 |
| **PN vs AN** | **Probe-Level** | 40,197 | **0** (0.00%) | **0** (0.00%) | 0 | 0 |
| | **Gene-Level** | 25,518 | **0** (0.00%) | **0** (0.00%) | 0 | 0 |

### Top Differentially Expressed Transcripts
- **Upregulated:**
  - `SSPO` (Spondin 1 / SCO-spondin): $\log_2\text{FC} = +1.954$, moderated $t = 5.956$, $\text{FDR} = 3.25 \times 10^{-5}$
  - `NNAT` (Neuronatin): $\log_2\text{FC} = +1.937$, moderated $t = 5.798$, $\text{FDR} = 4.90 \times 10^{-5}$
  - `P15RS` (Cyclin-dependent kinase inhibitor 2B-related): $\log_2\text{FC} = +1.786$, moderated $t = 5.638$, $\text{FDR} = 7.90 \times 10^{-5}$
  - `CLU` (Clusterin): $\log_2\text{FC} = +1.439$, moderated $t = 5.799$, $\text{FDR} = 4.90 \times 10^{-5}$
  - `MALL` (Mal, T-cell differentiation protein-like): $\log_2\text{FC} = +1.344$, moderated $t = 5.799$, $\text{FDR} = 4.90 \times 10^{-5}$
- **Downregulated:**
  - `ATP1B4` (ATPase $\text{Na}^+/\text{K}^+$ transporting beta 4): $\log_2\text{FC} = -4.308$, moderated $t = -11.891$, $\text{FDR} = 2.68 \times 10^{-11}$
  - `KLRA1` (Killer cell lectin-like receptor A1): $\log_2\text{FC} = -4.289$, moderated $t = -11.134$, $\text{FDR} = 1.29 \times 10^{-10}$
  - `GAPDH`: $\log_2\text{FC} = -3.452$, moderated $t = -10.860$, $\text{FDR} = 2.02 \times 10^{-10}$
  - `DPP3`: $\log_2\text{FC} = -2.879$, moderated $t = -10.712$, $\text{FDR} = 2.45 \times 10^{-10}$

---

## 3. Coordinated Pathways & Interactome Modules

- **Ranked GSEA:** Confirmed coordinate shifts in purine metabolism ($p_{\text{adj}} = 3.52 \times 10^{-11}$), unfolded protein response ($p_{\text{adj}} = 2.09 \times 10^{-8}$), glycolysis ($p_{\text{adj}} = 6.18 \times 10^{-8}$), and JAK-STAT signaling ($p_{\text{adj}} = 4.09 \times 10^{-7}$).
- **STRING PPI Network:** 45 candidate nodes, 13 verified interaction edges ($\ge 0.400$ confidence). Candidate hub proteins identified by degree and closeness centrality: `GAPDH` (deg 5), `ACTB` (deg 5), `CSF3` (deg 3), `LTF` (deg 3), and `CTSD` (deg 2).
