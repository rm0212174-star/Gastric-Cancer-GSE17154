# METHODOLOGY AND COMPUTATIONAL PROTOCOL

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Framework:** Python 3.13 / R-compatible Biostatistical Modeling  

---

## 1. Data Retrieval and Preprocessing

1. **NCBI GEO Extraction:** Official series matrix `GSE17154_series_matrix.txt.gz` and platform annotation `GPL6699_family.soft.gz` were retrieved via HTTPS from the NCBI GEO repository.
2. **Measurement Chemistry:** Processed data represent normalized $\log_2(\text{Cy5}/\text{Cy3})$ ratios where Cy5 = patient RNA and Cy3 = Stratagene Universal Human Reference RNA (UHRR).
3. **No Double-Log Transformation:** Values are already on the $\log_2$ ratio scale. No secondary log transformation was performed.
4. **Missing Value Imputation:** Exactly 1 missing value (Probe ID 24 in `GSM429144`) was imputed using the probe-level mean ($\mu = -0.0497$).

---

## 2. Probe Annotation and Control Filtering

- **Total Array Probes:** 44,544
- **Technical Control Spot Removal:** 4,347 spots (negative controls, BrightCorner alignment probes, structural spots) were flagged and excluded using the official GPL6699 SOFT table.
- **Experimental Feature Space:** 40,197 probes mapped 100% to unique Entrez / Gene Symbols representing 25,518 unique human genes.

---

## 3. Empirical Bayes Linear Modeling (`limma`)

1. **Design Matrix:** Because individual patient IDs were omitted in public records and sample counts are asymmetrical ($24 \neq 20$), an **unpaired 3-group design** (`~ 0 + Group`) was formulated with coefficients $\beta_{\text{Cancer}}$, $\beta_{\text{PN}}$, and $\beta_{\text{AN}}$.
2. **Variance Moderation:** Residual sample variances were moderated toward an overarching prior variance ($s_0^2 = 0.0340$, $d_0 = 2.15$), yielding moderated degrees of freedom $d_{\text{total}} = 48.15$.
3. **Hypothesis Testing:** Moderated $t$-statistics and $p$-values were evaluated against Student's $t$-distribution and adjusted for multiple testing using the Benjamini-Hochberg False Discovery Rate (FDR).
4. **Contrasts Evaluated:**
   - Contrast 1: $\text{Cancer} - \text{Paired\_Normal\_PN}$
   - Contrast 2: $\text{Cancer} - \text{Apparently\_Normal\_AN}$
   - Contrast 3: $\text{Paired\_Normal\_PN} - \text{Apparently\_Normal\_AN}$
5. **Gene-Level Summarization:** For genes with multiple probes, the probe exhibiting the maximum absolute moderated $t$-statistic was selected as the representative gene transcript.

---

## 4. Systems Biology & Network Analysis

1. **Over-Representation Analysis (ORA):** Hypergeometric testing of 595 strict DEGs against the background universe of 25,518 unique genes across GO BP/MF/CC, KEGG (2021), and Reactome (2022).
2. **Continuous Ranked GSEA:** Coordinate enrichment testing across all 25,518 genes ranked by moderated $t$-statistic.
3. **Protein-Protein Interaction Network:** Interrogated STRING v12.5 (*Homo sapiens*, confidence $\ge 0.400$) using NetworkX to compute degree and closeness centrality.
