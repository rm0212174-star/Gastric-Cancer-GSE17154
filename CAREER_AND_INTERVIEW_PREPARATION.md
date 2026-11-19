# PROFESSIONAL CAREER, RESUME, AND INTERVIEW PREPARATION GUIDE (STAGE 15)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Target Roles:** Bioinformatics Analyst, Computational Biologist, Scientific Data Scientist, Genomics Data Analyst  
**Audience Level:** MSc Biotechnology Graduate Portfolio  

---

## 1. Resume Specifications

### Recommended Project Title for Resume
**Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer (GEO GSE17154)**

### 4 Impact-Driven Resume Bullet Points
- **Transcriptomic Modeling:** Analyzed real Agilent 4x44K two-colour microarray transcriptomes (GSE17154, $N = 49$) across gastric adenocarcinoma, paired normal mucosa, and healthy endoscopy controls using empirical Bayes linear modeling (`limma`).
- **Feature Engineering & Disambiguation:** Filtered 4,347 control probes and implemented an automated probe-to-gene aggregation pipeline across 40,197 probes, mapping 25,518 unique human genes and identifying 595 strict unique DEGs ($|\log_2\text{FC}| \ge 1.0$, $\text{FDR} < 0.05$).
- **Systems Biology & Networks:** Executed ranked GSEA across 25,518 genes, detecting coordinate shifts in purine metabolism ($p_{\text{adj}} = 3.52 \times 10^{-11}$) and unfolded protein response ($p_{\text{adj}} = 2.09 \times 10^{-8}$); mapped protein interactome topology in STRING v12.5 (13 edges, candidate hub genes `GAPDH`, `ACTB`, `CSF3`, `LTF`, `CTSD`).
- **Reproducibility & Testing:** Built an automated 9-step reproducible batch pipeline (`run_pipeline.bat` / `.sh`) paired with unit test verification (`unittest`), ensuring 100% test coverage across sample counts, FDR bounds, and deliverable integrity.

### Demonstrated Technical Skills
- **Languages:** Python (Pandas, NumPy, SciPy, Matplotlib, NetworkX), R / Bioconductor (`limma`, `Biobase`), Shell / Batch scripting.
- **Bioinformatics Domains:** Microarray Quality Control, Microarray Probe Annotation (GPL6699), Differential Gene Expression, Multiple Hypothesis Testing (Benjamini-Hochberg FDR), Over-Representation Analysis (ORA), Ranked Gene-Set Enrichment Analysis (GSEA), Protein-Protein Interaction (STRING v12.5), Network Centrality.
- **Biostatistics & Engineering:** Empirical Bayes Shrinkage, Dimensionality Reduction (PCA), Hierarchical Clustering, Unit Testing, Checksum Auditing, Automated Pipelines.

---

## 2. Professional Online Profiles

### GitHub Project Description (Repository About Section)
> End-to-end reproducible bioinformatics analysis of gastric adenocarcinoma using real Agilent microarray transcriptomics from NCBI GEO GSE17154 (49 clinical samples, 40,197 probes). Implements limma empirical Bayes modeling, probe-to-gene aggregation, ranked GSEA, STRING v12.5 PPI networks, and automated test suite.

### LinkedIn Project Description
> **Integrated Transcriptomic and Systems Biology Analysis of Gastric Adenocarcinoma**  
> Conducted a rigorous, reproducible bioinformatics investigation into gastric adenocarcinoma using empirical microarray data from NCBI GEO GSE17154.  
> - Evaluated 49 clinical samples across tumor, paired normal, and healthy mucosal biopsies.  
> - Formulated an unpaired empirical Bayes moderated linear model (`limma`) to characterize 595 strict differentially expressed genes (e.g., `SSPO`, `NNAT`, `CLU`, `ATP1B4`).  
> - Identified coordinate metabolic and stress pathway reprogramming via continuous ranked GSEA (Purine Metabolism $p_{\text{adj}} < 10^{-10}$, UPR $p_{\text{adj}} < 10^{-7}$).  
> - Mapped interactome connectivity using STRING v12.5 and packaged the entire workflow into a one-click automated pipeline with 100% unit-test pass rate.

---

## 3. Interview Presentation Scripts

### 5-Minute Elevator Presentation Script
> *"For my major computational biology research project, I investigated transcriptomic dysregulation in gastric adenocarcinoma using real experimental data from NCBI GEO dataset GSE17154.*  
> *The cohort consists of 49 clinical samples profiled on an Agilent two-colour microarray platform: 24 gastric adenocarcinomas, 20 non-tumorous mucosal biopsies from the same stomach, and 5 healthy endoscopy controls.*  
> *After auditing the public records, I verified that patient-level identifiers were omitted, so I modeled the data using an unpaired three-group empirical Bayes design in limma rather than artificially forcing a matched-pair test.*  
> *After filtering 4,347 technical control spots, I evaluated 40,197 experimental probes mapped to 25,518 unique human genes. Using a maximum absolute t-statistic aggregation strategy, I identified 595 strict unique differentially expressed genes in tumors versus normal mucosa, including upregulation of SCO-spondin (SSPO), Neuronatin (NNAT), and Clusterin (CLU), and severe repression of epithelial transport proteins like ATP1B4.*  
> *Importantly, comparing paired normal mucosa to healthy endoscopic controls revealed zero significant DEGs at FDR 0.05, though with N=5 in the control group, I documented that statistical power is limited to detect subtle field defects.*  
> *Through continuous ranked GSEA across all 25,518 genes, I detected coordinate activation of purine metabolism and unfolded protein response pathways. I then constructed a STRING protein interaction network to identify candidate hub genes like GAPDH and CTSD.*  
> *Finally, I engineered the workflow into a reproducible 9-step pipeline with an automated test suite verifying sample metadata, FDR bounds, and deliverable integrity with 100% pass rates."*

### 10-Minute Detailed Technical Presentation Structure
1. **Introduction & Rationale (2 mins):** Gastric cancer clinical burden; choice of GSE17154 (Agilent 4x44K common reference design against Stratagene UHRR); need for reproducible auditing.
2. **Quality Control & Study Design (2 mins):** 49 arrays, 1 missing value out of 2.18M data points; PCA separating tumor from normal along PC1 (19.5%) and PC2 (18.8%); why unpaired modeling is statistically mandatory due to anonymous GEO metadata.
3. **Differential Expression & Feature Disambiguation (2 mins):** 4,347 control spots filtered; probe-level (633 DEGs) vs gene-level (595 DEGs) disambiguation; key up/down transcripts.
4. **Functional Pathways & Systems Interactome (2 mins):** Contrast between thresholded ORA and continuous ranked GSEA; ER stress (UPR) and purine metabolism; STRING v12.5 network topology and why hub genes are computational hypotheses, not proven biomarkers.
5. **Reproducibility, Automated Testing & Future Directions (2 mins):** 9-step pipeline, 6 automated test assertions (`unittest`), documented limitations, and cross-platform validation avenues with TCGA-STAD.

---

## 4. Technical Interview Questions & Answers

### Q1: Why did you choose GSE17154 and what are its technological characteristics?
**Answer:** GSE17154 is a well-characterized gastric cancer dataset with 49 clinical samples including tumor, tumor-adjacent mucosal biopsies from cancer patients, and healthy endoscopy controls. It uses the Agilent 4x44K two-colour microarray (GPL6699) where patient tissue (Cy5) is competitively hybridized against Stratagene Universal Human Reference RNA (Cy3). The reported values are normalized $\log_2(\text{Cy5}/\text{Cy3})$ ratios, making samples directly comparable across arrays.

### Q2: Why did you use an unpaired design rather than a paired test for the 20 paired normal samples?
**Answer:** While the 20 normal mucosa samples biologically originate from the same stomach as cancer patients, the public GEO record provides no deterministic one-to-one patient linkage tags (`!Sample_description = "no additional information"`), and the sample numbers are asymmetrical (24 cancers vs 20 normal biopsies). Arbitrarily assigning paired links would fabricate synthetic pairings and introduce false degrees of freedom. In accordance with the original study (Rajkumar et al., 2010), an unpaired three-group linear model (`~ 0 + Group`) was the only mathematically and scientifically valid formulation.

### Q3: What is the biological meaning of a Log2 Fold Change and an FDR-adjusted P-value?
**Answer:** A $\log_2\text{FC} = +1.0$ represents a 2-fold increase in transcript abundance in cancer relative to normal tissue, while $\log_2\text{FC} = -1.0$ represents a 50% reduction (0.5-fold). Because 40,197 hypothesis tests were performed simultaneously, using raw $p$-values would lead to hundreds of false discoveries. The False Discovery Rate (FDR) adjusted via the Benjamini-Hochberg procedure controls the expected proportion of false positives among all rejected null hypotheses. An $\text{FDR} < 0.05$ guarantees that fewer than 5% of declared DEGs are expected to be false discoveries.

### Q4: Why did you choose `limma` over standard Student's t-tests?
**Answer:** In microarray transcriptomics, the number of genes ($N = 40,197$) vastly exceeds the sample size ($N = 49$). Individual gene variance estimates can be unstable due to small sample size. `limma` employs an empirical Bayes hierarchical model that shrinks gene-specific sample variances toward a common pooled prior variance ($s_0^2 = 0.0340$, $d_0 = 2.15$). This borrows statistical strength across the entire array, yielding moderated $t$-statistics with higher statistical power and fewer false positives.

### Q5: What does PCA demonstrate about this dataset?
**Answer:** PCA decomposes the 44,544-dimensional probe space into orthogonal axes of maximum variance. PC1 (19.52%) cleanly separates malignant tumors from non-malignant mucosa. PC2 (18.82%) captures tumor-intrinsic biological heterogeneity, with advanced metastatic cases projecting furthest. This demonstrates that global transcriptional variance is dominated by true disease biology rather than technical batch artifacts.

### Q6: Why did Over-Representation Analysis (ORA) and ranked GSEA give different results?
**Answer:** ORA performs a hypergeometric test on a pre-filtered list of 595 strict DEGs against the background universe of 25,518 genes. While terms like JAK-STAT and Cell Cycle reached nominal significance ($p < 0.01$), after multiple-testing correction across hundreds of pathway categories, individual ORA FDR values were non-significant. In contrast, ranked GSEA utilizes the continuous distribution of all 25,518 genes ranked by moderated $t$-statistic. This sensitive, non-thresholded approach detected coordinate, cumulative shifts in purine metabolism ($p_{\text{adj}} = 3.52 \times 10^{-11}$) and unfolded protein response ($p_{\text{adj}} = 2.09 \times 10^{-8}$).

### Q7: Why are STRING PPI hub genes considered candidate hypotheses rather than clinical biomarkers?
**Answer:** Network hubs like `GAPDH` and `ACTB` have high degree centrality (degree 5) largely because they are ubiquitous structural and metabolic proteins with extensive literature annotations. Their connectivity reflects pleiotropy rather than driver oncogene status. In computational biology, in silico network centrality must never be conflated with clinical actionability without orthogonal wet-lab assays (RT-qPCR, Western blot, IHC, and prospective multi-cohort survival studies).

### Q8: What are the main limitations of this dataset?
**Answer:** First, the two-colour microarray platform has dynamic range and hybridization compression limits compared to modern digital RNA-seq. Second, the healthy endoscopy control group is small ($N = 5$), which limits statistical power to detect subtle field defect differences in `PN vs AN`. Third, GSE17154 records static outcomes (`NED` vs `failed`) without longitudinal time-to-event follow-up intervals, which legitimately precludes Kaplan-Meier survival curves and Cox proportional hazards regression.
