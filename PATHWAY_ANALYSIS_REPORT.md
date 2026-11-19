# FUNCTIONAL ENRICHMENT AND PATHWAY ANALYSIS REPORT (STAGE 6)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  
**Background Gene Universe ($N$):** 25,518 unique mapped human genes from GPL6699  
**Tested Gene Subsets:** 595 strict unique DEGs (ORA) and 25,518 ranked genes (GSEA)  

---

## 1. Over-Representation Analysis (ORA) vs Continuous Ranked GSEA

To prevent inflated biological claims, functional enrichment was evaluated using two complementary biostatistical strategies:

1. **Discrete Over-Representation Analysis (ORA, Fisher's Exact Test / Hypergeometric):**
   - **Target Query:** The 595 strict differentially expressed genes ($|\log_2\text{FC}| \ge 1.0$ and $\text{FDR} < 0.05$).
   - **Background Universe:** All 25,518 unique genes represented on the GPL6699 array.
   - **Top KEGG Findings:** `JAK-STAT signaling pathway` ($p = 0.0039$), `Cell cycle regulation` ($p = 0.0076$), `Viral carcinogenesis` ($p = 0.0084$).
   - **Top Reactome Findings:** `Unfolded Protein Response (UPR)` ($p = 0.0081$), `Cellular response to stress` ($p = 0.012$).
   - **Top GO Findings:** `filopodium membrane` (GO:0031527, $p = 0.0012$, $\text{FDR} = 0.078$), `endosome lumen` ($p = 0.0021$).
   - **Multiple Testing Caveat:** After Benjamini-Hochberg adjustment across hundreds of pathway categories, individual ORA terms exceed FDR $0.05$. These terms are reported as nominal candidates ($p < 0.01$).

2. **Continuous Ranked Gene-Set Enrichment Analysis (GSEA):**
   - **Input:** All 25,518 genes ranked by moderated $t$-statistic from the empirical Bayes model.
   - **Results:** Evaluates coordinate, cumulative shifts across entire pathways without threshold truncations.
   - **Significantly Dysregulated Gene Sets:**
     - *Purine metabolism:* $p_{\text{adj}} = 3.52 \times 10^{-11}$
     - *Human T-cell leukemia virus 1 infection:* $p_{\text{adj}} = 1.49 \times 10^{-9}$
     - *Hepatocellular carcinoma:* $p_{\text{adj}} = 4.31 \times 10^{-9}$
     - *Unfolded Protein Response (UPR):* $p_{\text{adj}} = 2.09 \times 10^{-8}$
     - *Glycolysis / Gluconeogenesis:* $p_{\text{adj}} = 6.18 \times 10^{-8}$
     - *JAK-STAT signaling pathway:* $p_{\text{adj}} = 4.09 \times 10^{-7}$

---

## 2. Deliverable File Inventory

| Result Table / Figure | File Path | Key Metrics |
| :--- | :--- | :--- |
| **GO Biological Process** | [GO_BP_Enrichment.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/Enrichment/GO_BP_Enrichment.csv) | 480 terms evaluated |
| **GO Molecular Function** | [GO_MF_Enrichment.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/Enrichment/GO_MF_Enrichment.csv) | 442 terms evaluated |
| **GO Cellular Component** | [GO_CC_Enrichment.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/Enrichment/GO_CC_Enrichment.csv) | 226 terms evaluated |
| **KEGG Pathways** | [KEGG_Enrichment.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/Enrichment/KEGG_Enrichment.csv) | 250 pathways evaluated |
| **Reactome Pathways** | [Reactome_Enrichment.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/Enrichment/Reactome_Enrichment.csv) | 903 pathways evaluated |
| **Ranked GSEA Results** | [GSEA_Results.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/results/Enrichment/GSEA_Results.csv) | Top coordinate gene sets |
| **Combined Figure** | [Enrichment_Dotplots.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/Enrichment_Dotplots.png) | 4-panel multi-database plot |
