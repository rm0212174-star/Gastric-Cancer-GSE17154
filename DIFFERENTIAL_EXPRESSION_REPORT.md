# DIFFERENTIAL GENE EXPRESSION ANALYSIS REPORT (STAGE 5)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  
**Platform Accession:** GPL6699 (40,197 Experimental Probes, 25,518 Unique Human Genes)  
**Methodology:** Empirical Bayes Moderated Linear Modeling (`limma`, Smyth 2004)  

---

## 1. Linear Modeling & Contrast Formulation

- **Design Formula:** `~ 0 + Group` (Unpaired 3-Group Design)
- **Groups:** `CANCER` ($N = 24$), `Paired_Normal_PN` ($N = 20$), `Apparently_Normal_AN` ($N = 5$)
- **Contrasts:**
  - $C_1$: $\text{Cancer} - \text{Paired\_Normal\_PN}$
  - $C_2$: $\text{Cancer} - \text{Apparently\_Normal\_AN}$
  - $C_3$: $\text{Paired\_Normal\_PN} - \text{Apparently\_Normal\_AN}$
- **Empirical Bayes Variance Shrinkage:** Prior degrees of freedom $d_0 = 2.15$, prior variance $s_0^2 = 0.0340$, moderated degrees of freedom $d_{\text{total}} = 48.15$.

---

## 2. Statistical Findings: Probe-Level vs Gene-Level Disambiguation

### 2.1 Probe-Level Summary (40,197 Experimental Spots)
| Contrast | Tested Probes | FDR < 0.05 | Strict DEGs (FDR < 0.05 & \|Log2FC\| $\ge$ 1.0) | Up-regulated (Log2FC $\ge$ 1.0) | Down-regulated (Log2FC $\le$ -1.0) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Cancer vs Paired Normal** | 40,197 | 2,886 (7.18%) | **633** (1.57%) | 60 | 573 |
| **Cancer vs Apparently Normal** | 40,197 | 1,314 (3.27%) | **643** (1.60%) | 93 | 550 |
| **Paired Normal vs Apparently Normal** | 40,197 | **0** (0.00%) | **0** (0.00%) | 0 | 0 |

### 2.2 Gene-Level Summarized Results (25,518 Unique Human Genes, Max \|t\| Aggregation)
| Contrast | Unique Genes | FDR < 0.05 | Strict DEGs (FDR < 0.05 & \|Log2FC\| $\ge$ 1.0) | Up-regulated Genes | Down-regulated Genes |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Cancer vs Paired Normal** | 25,518 | 2,625 (10.29%) | **595** (2.33%) | 52 | 543 |
| **Cancer vs Apparently Normal** | 25,518 | 1,232 (4.83%) | **605** (2.37%) | 81 | 524 |
| **Paired Normal vs Apparently Normal** | 25,518 | **0** (0.00%) | **0** (0.00%) | 0 | 0 |

---

## 3. Top Ranked Differentially Expressed Genes

### Top Up-regulated Transcripts in Gastric Adenocarcinoma
1. `SSPO` (Spondin 1 / SCO-spondin): $\log_2\text{FC} = +1.954$, moderated $t = 5.956$, $\text{FDR} = 3.25 \times 10^{-5}$
2. `NNAT` (Neuronatin): $\log_2\text{FC} = +1.937$, moderated $t = 5.798$, $\text{FDR} = 4.90 \times 10^{-5}$
3. `P15RS` (Cyclin-dependent kinase inhibitor 2B-related / RPRD1A): $\log_2\text{FC} = +1.786$, moderated $t = 5.638$, $\text{FDR} = 7.90 \times 10^{-5}$
4. `CLU` (Clusterin): $\log_2\text{FC} = +1.439$, moderated $t = 5.799$, $\text{FDR} = 4.90 \times 10^{-5}$
5. `MALL` (Mal, T-cell differentiation protein-like): $\log_2\text{FC} = +1.344$, moderated $t = 5.799$, $\text{FDR} = 4.90 \times 10^{-5}$
6. `SCARA3` (Scavenger receptor class A member 3): $\log_2\text{FC} = +1.068$, moderated $t = 5.923$, $\text{FDR} = 3.50 \times 10^{-5}$

### Top Down-regulated Transcripts in Gastric Adenocarcinoma
1. `ATP1B4` (ATPase $\text{Na}^+/\text{K}^+$ transporting beta 4): $\log_2\text{FC} = -4.308$, moderated $t = -11.891$, $\text{FDR} = 2.68 \times 10^{-11}$
2. `KLRA1` (Killer cell lectin-like receptor A1): $\log_2\text{FC} = -4.289$, moderated $t = -11.134$, $\text{FDR} = 1.29 \times 10^{-10}$
3. `GAPDH` (Glyceraldehyde-3-phosphate dehydrogenase probe): $\log_2\text{FC} = -3.452$, moderated $t = -10.860$, $\text{FDR} = 2.02 \times 10^{-10}$
4. `DPP3` (Dipeptidyl peptidase 3): $\log_2\text{FC} = -2.879$, moderated $t = -10.712$, $\text{FDR} = 2.45 \times 10^{-10}$
5. `CPEB2` (Cytoplasmic polyadenylation element binding protein 2): $\log_2\text{FC} = -2.480$, moderated $t = -10.525$, $\text{FDR} = 3.57 \times 10^{-10}$

---

## 4. Visualizations & Result Files

| Contrast | Volcano Plot | MA Plot | Top 50 DEG Heatmap | Full DEG Table | Strict DEG Table |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cancer vs PN** | [Volcano_Cancer_vs_PN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Volcano_Cancer_vs_PN.png) | [MA_Cancer_vs_PN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/MA_Cancer_vs_PN.png) | [Heatmap_Top50_Cancer_vs_PN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Heatmap_Top50_Cancer_vs_PN.png) | [Full CSV](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/DEG/DEG_Cancer_vs_PN_Full.csv) | [Strict CSV](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/DEG/DEG_Cancer_vs_PN_Gene_Level_Strict_FDR05_FC2.csv) |
| **Cancer vs AN** | [Volcano_Cancer_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Volcano_Cancer_vs_AN.png) | [MA_Cancer_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/MA_Cancer_vs_AN.png) | [Heatmap_Top50_Cancer_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Heatmap_Top50_Cancer_vs_AN.png) | [Full CSV](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/DEG/DEG_Cancer_vs_AN_Full.csv) | [Strict CSV](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/DEG/DEG_Cancer_vs_AN_Gene_Level_Strict_FDR05_FC2.csv) |
| **PN vs AN** | [Volcano_PN_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Volcano_PN_vs_AN.png) | [MA_PN_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/MA_PN_vs_AN.png) | [Heatmap_Top50_PN_vs_AN.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Heatmap_Top50_PN_vs_AN.png) | [Full CSV](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/DEG/DEG_PN_vs_AN_Full.csv) | Min FDR = 0.2601 (0 DEGs) |
