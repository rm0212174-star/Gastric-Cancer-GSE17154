# FINAL CV PROJECT DESCRIPTION & PROFESSIONAL PROFILES

**Target Roles:** Bioinformatics Analyst | Computational Biologist | Scientific Data Scientist | Genomics Data Analyst  
**Candidate Qualification:** MSc Biotechnology Graduate  

---

## 1. Resume Entry (Concise & Professional)

### Project Heading
**Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer (GEO GSE17154)**  
*MSc Biotechnology Independent Bioinformatics Research Project* | *Nov 2026*  
[GitHub Repository Link] | Tools: Python, R/Bioconductor (`limma`), Linux Shell, Batch Scripting, NetworkX

### Bullet Points for Resume (Choose 3–4)
- **Empirical Transcriptomic Modeling:** Re-analyzed raw Agilent 4x44K two-colour microarray transcriptomes (NCBI GEO GSE17154, $N = 49$) across gastric adenocarcinoma, paired normal mucosa, and healthy controls using empirical Bayes linear modeling (`limma`).
- **Feature Engineering & Disambiguation:** Filtered 4,347 control probes and implemented an automated probe-to-gene aggregation pipeline across 40,197 probes, mapping 25,518 unique human genes and identifying 595 strict unique DEGs ($|\log_2\text{FC}| \ge 1.0$, $\text{FDR} < 0.05$).
- **Systems Biology & Networks:** Executed continuous ranked GSEA across 25,518 genes, detecting coordinate enrichment in purine metabolism ($p_{\text{adj}} = 3.52 \times 10^{-11}$) and unfolded protein response ($p_{\text{adj}} = 2.09 \times 10^{-8}$); mapped protein interactome topology in STRING v12.5 (13 edges, candidate hub genes `GAPDH`, `ACTB`, `CSF3`, `LTF`, `CTSD`).
- **Production Reproducibility:** Engineered an automated 9-step batch execution pipeline (`run_pipeline.bat` / `.sh`) backed by an automated unit-test suite (`unittest`) with 100% test pass rate across sample counts, FDR bounds, and deliverable presence.

---

## 2. LinkedIn Project Entry

### Project Title
**Integrated Transcriptomic and Network-Based Analysis of Gastric Adenocarcinoma**

### Description
> Conducted a rigorous, reproducible bioinformatics investigation into gastric adenocarcinoma using empirical microarray data from NCBI GEO GSE17154 (49 clinical samples, 44,544 probes).
> 
> Key Achievements:
> - Audited public repository records, identifying the absence of patient-level pairing identifiers, and formulated an unpaired 3-group empirical Bayes linear model (`limma`).
> - Filtered 4,347 technical control spots and aggregated 40,197 experimental probes to 25,518 unique human genes, characterizing 595 strict unique DEGs (e.g., `SSPO`, `NNAT`, `CLU`, `ATP1B4`).
> - Performed continuous ranked GSEA, uncovering coordinate dysregulation in purine metabolism ($p_{\text{adj}} < 10^{-10}$) and unfolded protein response ($p_{\text{adj}} < 10^{-7}$).
> - Mapped network connectivity via STRING v12.5 and packaged the entire analytical workflow into an automated one-click pipeline with a 6-test unit validation suite.

---

## 3. GitHub About Summary (160 characters)
> End-to-end reproducible bioinformatics analysis of gastric cancer (GSE17154, 49 samples). Implements limma eBayes, probe-to-gene aggregation, GSEA, and STRING PPI.
