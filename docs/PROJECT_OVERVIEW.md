# PROJECT OVERVIEW

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Primary Dataset:** NCBI GEO Accession [GSE17154](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17154)  
**Microarray Platform:** Agilent Whole Human Genome Microarray 4x44K [GPL6699](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL6699)  
**Primary Reference:** Rajkumar et al., *Cancer Cell International* 2010, 10:45 ([PMID: 21092330](https://pubmed.ncbi.nlm.nih.gov/21092330/), [PMCID: PMC3004887](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3004887/))  
**Academic Target:** MSc Biotechnology Bioinformatics Research Portfolio  
**Audit Status:** **`VERIFIED WITH DOCUMENTED LIMITATIONS`**

---

## 1. Scientific Background & Research Question

Gastric adenocarcinoma is a leading cause of worldwide cancer mortality, characterized by profound clinical heterogeneity and late-stage presentation. While extensive transcriptomic data exist in public archives, translational bioinformatics frequently suffers from unverified sample pairing, lack of feature disambiguation, and premature claims of diagnostic biomarkers.

**Central Research Question:**  
What are the genuine differentially expressed transcripts, coordinated biological pathways, and interactome hub modules that distinguish primary gastric adenocarcinoma from non-malignant mucosa, when evaluated using an empirically validated, unpaired statistical framework on GSE17154?

---

## 2. Cohort Composition (49 Clinical Samples)

The dataset comprises 49 hybridization assays across three biological groups:
- **Gastric Adenocarcinoma (`CANCER`, $N = 24$):** Biopsies of primary gastric tumors (23 adenocarcinomas, 1 neuroendocrine carcinoma).
- **Paired Normal Mucosa (`Paired_Normal_PN`, $N = 20$):** Non-malignant mucosal biopsies sampled from the **same stomach** as the cancer, remote from the tumor margin, verified tumor-free by frozen section histopathology.
- **Apparently Normal Controls (`Apparently_Normal_AN`, $N = 5$):** Gastric mucosal biopsies from healthy volunteer endoscopy donors.

---

## 3. High-Level Summary of Findings

1. **Feature Space:** 44,544 total hybridization spots were filtered to remove 4,347 technical controls, retaining **40,197 experimental probes** representing **25,518 unique human genes**.
2. **Differential Expression:**
   - *Cancer vs Paired Normal:* **633 strict probes** ($|\log_2\text{FC}| \ge 1.0$, $\text{FDR} < 0.05$), summarizing to **595 unique genes** (52 Up, 543 Down).
   - *Cancer vs Apparently Normal:* **643 strict probes**, summarizing to **605 unique genes** (81 Up, 524 Down).
   - *Paired Normal vs Apparently Normal:* **0 DEGs** ($\text{min FDR} = 0.2601$).
3. **Biological Dysregulation:** Ranked GSEA across all 25,518 genes identified significant coordinate enrichment in purine metabolism ($p_{\text{adj}} = 3.52 \times 10^{-11}$), unfolded protein response ($p_{\text{adj}} = 2.09 \times 10^{-8}$), and glycolysis ($p_{\text{adj}} = 6.18 \times 10^{-8}$).
4. **Interactome Topology:** STRING v12.5 network analysis identified candidate hub genes including `GAPDH`, `ACTB`, `CSF3`, `LTF`, and `CTSD`.
