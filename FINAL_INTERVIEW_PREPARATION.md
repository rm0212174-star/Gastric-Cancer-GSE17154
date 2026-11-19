# FINAL TECHNICAL INTERVIEW PREPARATION GUIDE (20 IN-DEPTH QUESTIONS & ANSWERS)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Target Roles:** Bioinformatics Analyst | Computational Biologist | Scientific Data Scientist  

---

### Question 1: What is dataset GSE17154 and why was it selected for this investigation?
**Answer:** GSE17154 is a well-curated public transcriptomic dataset from the Cancer Institute (WIA), Chennai, India, published by Rajkumar et al. (2010) in *Cancer Cell International*. It interrogates 49 clinical specimens across three distinct biological cohorts: 24 primary gastric adenocarcinomas, 20 non-tumorous gastric mucosal biopsies from cancer stomachs, and 5 healthy endoscopy controls. It was selected because it provides genuine clinical tissue comparisons on a standardized platform (Agilent 4x44K) with published histopathological validation.

### Question 2: What microarray technology was used, and what does the expression metric represent?
**Answer:** The dataset utilizes the Agilent Whole Human Genome Microarray 4x44K (GPL6699, G4112F). It employs a competitive two-colour hybridization design where clinical specimen total RNA is labeled with Cy5 (red channel) and Stratagene Universal Human Reference RNA (UHRR) is labeled with Cy3 (green channel). The reported processed metric `VALUE` represents normalized $\log_2(\text{Cy5}/\text{Cy3})$ ratios median-centered across each array.

### Question 3: Why did you not apply an additional log2 transformation to the expression matrix?
**Answer:** Applying an additional logarithmic transformation to data already expressed as $\log_2$ ratios would mathematically corrupt the distribution. Since the values are $\log_2(\text{Cy5}/\text{Cy3})$, negative values represent down-regulation relative to UHRR and positive values represent up-regulation. Applying a second log transformation would produce `NaN` values for all negative ratios and compress positive ratios, invalidating the empirical linear model.

### Question 4: How did you evaluate quality control and handle missing data?
**Answer:** Quality control was conducted across all 44,544 probes and 49 arrays (2,182,656 total data points). Boxplots confirmed uniform median-centering at 0.0000, and density plots showed smooth unimodal distributions. Only 1 missing value was detected (Probe 24 in sample GSM429144), which was imputed using the probe-level mean across the remaining 48 samples ($\mu = -0.0497$). No sample or probe was discarded due to missingness.

### Question 5: What did Principal Component Analysis (PCA) reveal about the clinical specimens?
**Answer:** PCA decomposed the 44,544 probe dimensions into orthogonal components of variance. PC1 (19.52%) cleanly separated malignant adenocarcinoma from non-tumorous mucosa. PC2 (18.82%) captured tumor-intrinsic heterogeneity. Notably, advanced metastatic cases (`CANCER - 16` and `CANCER - 17`) projected to the far periphery of PC1/PC2 space, demonstrating that global variance reflects genuine cancer progression rather than technical batch artifacts.

### Question 6: What was your strategy for filtering platform probes?
**Answer:** Using the official GPL6699 platform specification and spot-level GPR data, we flagged and excluded 4,347 technical control spots (negative controls, BrightCorner spatial grid landmarks, and calibration mismatch spots). This left exactly 40,197 experimental probes. PCA comparing experimental probes alone versus all 44,544 spots showed near-perfect correlation ($r = 0.9926$), confirming that controls do not distort global structure but must be removed to avoid statistical artifacts in differential testing.

### Question 7: How did you handle the multi-probe gene problem in this array?
**Answer:** In GPL6699, 7,344 unique genes are interrogated by multiple probes (e.g., `ACTB` has 392 probes; housekeeping controls have 104 probes). To prevent multi-probe genes from dominating downstream enrichment and violating independent-sampling assumptions, we implemented a gene-level aggregation pipeline that selects the probe with the **maximum absolute moderated $t$-statistic** ($\max |t|$) per unique gene symbol.

### Question 8: Why do probe-level DEG counts differ from gene-level DEG counts?
**Answer:** In Cancer vs Paired Normal, probe-level analysis identified 633 strict DEGs ($|\log_2\text{FC}| \ge 1.0$, $\text{FDR} < 0.05$), whereas gene-level analysis identified 595 strict unique genes. The difference arises because multiple probes targeting the same gene (e.g., multiple probes for structural actin or metabolic enzymes) each pass the statistical cutoff. Gene-level aggregation collapses redundant probes into single biological transcripts.

### Question 9: Why did you use an unpaired statistical model rather than a paired model for the 20 paired normal samples?
**Answer:** While the 20 normal mucosa samples biologically originate from the same stomach as cancer patients, public GEO records provide no deterministic 1-to-1 patient linkage tags (`!Sample_description = 'no additional information'`). Furthermore, sample counts are asymmetrical ($N_{\text{Cancer}} = 24 \neq N_{\text{PN}} = 20$). Imposing a paired model would require arbitrarily inventing 20 patient pairings and discarding 4 cancer cases. In accordance with the original publication (Rajkumar et al., 2010), an **unpaired 3-group design** (`~ 0 + Group`) was the only scientifically defensible choice.

### Question 10: How does `limma` empirical Bayes modeling work, and why is it superior to ordinary Student's t-tests?
**Answer:** In high-dimensional transcriptomics where $P \gg N$ (40,197 probes vs 49 samples), gene-specific sample variance estimates ($s_g^2$) are unstable. `limma` fits a linear model and applies an empirical Bayes hierarchical model that shrinks individual gene variances toward an overarching prior variance ($s_0^2 = 0.0340$, $d_0 = 2.15$). This borrows information across all 40,197 probes, yielding moderated $t$-statistics with $48.15$ degrees of freedom, dramatically increasing statistical power and reducing false positives.

### Question 11: How were multiple testing corrections handled, and what does an FDR of 0.05 mean?
**Answer:** Because 40,197 simultaneous hypothesis tests were performed, raw $p$-values would yield hundreds of false discoveries. We applied the Benjamini-Hochberg (BH) False Discovery Rate (FDR) procedure. An adjusted $p$-value (FDR) threshold of $< 0.05$ guarantees that among all genes declared differentially expressed, fewer than 5% are expected to be false positives.

### Question 12: What did the comparison between Paired Normal and Apparently Normal mucosa (`PN vs AN`) show, and how do you interpret it?
**Answer:** Zero probes and zero unique genes achieved statistical significance at $\text{FDR} < 0.05$ (minimum FDR was $0.2601$). This confirms that non-malignant mucosa remote from the primary tumor does not exhibit gross transcriptomic remodeling comparable to frank neoplasia. However, because the control group comprises only $N = 5$ samples, statistical power is severely constrained; this failure to reject the null hypothesis cannot be interpreted as proving biological equivalence.

### Question 13: Why did discrete Over-Representation Analysis (ORA) and continuous ranked GSEA yield different results?
**Answer:** ORA performs a hypergeometric test on a thresholded subset of 595 strict DEGs against the background universe of 25,518 genes. While terms like JAK-STAT and Cell Cycle reached nominal significance ($p < 0.01$), after multiple-testing correction across hundreds of ontologies, individual ORA FDR values exceeded 0.05. In contrast, ranked GSEA uses the continuous distribution of all 25,518 genes ranked by moderated $t$-statistic. This sensitive, coordinate approach detected highly significant shifts in purine metabolism ($p_{\text{adj}} = 3.52 \times 10^{-11}$) and unfolded protein response ($p_{\text{adj}} = 2.09 \times 10^{-8}$).

### Question 14: What was the background gene universe used for functional enrichment, and why does it matter?
**Answer:** The background universe was strictly defined as the **25,518 unique human genes** represented by the experimental probes on GPL6699. Using the whole human genome (~40,000 genes) as a default background would artificially inflate statistical significance, because microarray platforms do not sample all human genes uniformly.

### Question 15: What is the biological function of `SSPO` and why is it upregulated in gastric cancer?
**Answer:** `SSPO` (SCO-spondin / Spondin 1, $\log_2\text{FC} = +1.954$, $\text{FDR} = 3.25 \times 10^{-5}$) encodes a large extracellular matrix glycoprotein containing multiple thrombospondin type 1 (TSR1) and von Willebrand factor type C domains. In gastric adenocarcinoma, aggressive desmoplastic stroma expansion and abnormal ECM cross-linking promote tumor cell adhesion, migration, and resistance to chemotherapeutic agents.

### Question 16: What is the significance of `NNAT` upregulation?
**Answer:** `NNAT` (Neuronatin, $\log_2\text{FC} = +1.937$, $\text{FDR} = 4.90 \times 10^{-5}$) encodes an endoplasmic reticulum proteolipid that regulates calcium channels and $\text{SERCA}$ pump activity. Elevated `NNAT` stimulates intracellular calcium signaling and activates the Unfolded Protein Response (UPR), enabling rapid tumor growth and survival under hypoxic stress.

### Question 17: Why is `ATP1B4` drastically downregulated in gastric adenocarcinoma?
**Answer:** `ATP1B4` ($\log_2\text{FC} = -4.308$, $\text{FDR} = 2.68 \times 10^{-11}$) is an integral subunit of the X,K-ATPase cation transport complex in mature gastric parietal and chief cells. Its profound repression highlights the loss of apical-basal polarity and terminal functional dedifferentiation of mature gastric epithelium during malignant transformation.

### Question 18: Why are STRING PPI hub genes like `GAPDH` and `ACTB` designated as computational candidates rather than clinical biomarkers?
**Answer:** Network hubs like `GAPDH` and `ACTB` possess high degree centrality (degree 5) primarily because they are ubiquitous structural and metabolic proteins with extensive historical literature annotations in STRING v12.5. Their high connectivity reflects biological pleiotropy rather than driver oncogene status. Claiming them as clinical biomarkers without prospective functional assays would violate translational research standards.

### Question 19: Why was longitudinal survival analysis (Kaplan-Meier, Cox regression) excluded?
**Answer:** NCBI GEO GSE17154 records discrete static outcome codes (`NED` vs `failed`) at the time of submission. It does not provide continuous time-to-event follow-up intervals (e.g., overall survival in months or right-censoring dates). Generating artificial survival curves without follow-up intervals would be fraudulent. Consequently, clinical analysis was strictly restricted to descriptive TNM stage and nuclear grade stratification.

### Question 20: How did you ensure automated reproducibility and code quality?
**Answer:** The entire analytical pipeline is packaged into modular scripts executed sequentially via `run_pipeline.bat` (Windows) and `run_pipeline.sh` (Linux), with automated exit-code checking. In addition, an automated test suite (`tests/test_pipeline_validation.py`) executes 6 unit tests asserting sample counts (49), probe dimensions (44,544 total, 40,197 experimental), FDR bounds ($[0, 1]$), exact DEG reproducibility, and deliverable non-emptiness, running live in under 0.4 seconds with a 100% pass rate.
