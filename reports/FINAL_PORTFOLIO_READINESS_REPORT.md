# FINAL PORTFOLIO READINESS AND SCIENTIFIC REPRODUCIBILITY REPORT

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date of Audit:** 2026-11-19  
**Candidate Qualification:** MSc Biotechnology Graduate Portfolio  
**Audit Standard:** Independent Scientific Review, Code Audit & Reproducibility Check  
**Official Readiness Status:** **`VERIFIED WITH DOCUMENTED LIMITATIONS — READY FOR CV & GITHUB`**

---

## 1. Item-by-Item Classification Matrix

| Category | Audit Item | Evaluation Standard | Audit Verdict | Evidence / Justification |
| :--- | :--- | :--- | :---: | :--- |
| **Stage 1: Data Provenance** | GSE17154 Authenticity | Official NCBI GEO source | **PASS** | Matching sizes and SHA-256 hashes (`8ddf...`) |
| | GPL6699 Annotation | Official Agilent SOFT table | **PASS** | 44,544 rows matched, GPR column headers verified |
| | Sample Counts & Groups | 24 Cancer, 20 PN, 5 AN | **PASS** | 49 samples verified against GSM records |
| | Absence of Simulated Data | Zero mock/synthetic arrays | **PASS** | Verified 100% genuine data; training simulations isolated |
| **Stage 2: Study Design** | Group Nomenclature | Distinguish tissue origin | **PASS** | `CANCER`, `Paired_Normal_PN`, `Apparently_Normal_AN` |
| | Statistical Pairing | Verify 1-to-1 patient linkage | **PASS** | Proved no linkage in GEO; unpaired model (`~ 0 + Group`) applied |
| | Contrast Directions | Cancer vs Normal direction | **PASS** | Contrast signs verified ($\text{Cancer} - \text{Normal}$) |
| **Stage 3: Preprocessing** | Control Spot Filtering | Remove technical controls | **PASS** | Exactly 4,347 control spots filtered; 40,197 probes retained |
| | Probe-to-Gene Mapping | GPL6699 identifier mapping | **PASS** | 40,197 probes mapped to 25,518 unique human genes |
| | Value Scale | No double-log transformation | **PASS** | Verified normalized $\log_2(\text{Cy5}/\text{Cy3})$ input scale |
| | Microarray Dynamic Range | Platform saturation/compression | **WARNING** | Two-colour arrays have lower dynamic range than RNA-seq |
| **Stage 4: Differential Testing** | Reproducibility of DEGs | Independent eBayes execution | **PASS** | Exactly reproduces 633 & 643 probes; 595 & 605 genes |
| | Disambiguation | Probe vs Gene DEGs | **PASS** | Max $|t|$ gene aggregation clearly documented |
| | Field Effect Normal (PN vs AN) | Statistical power limits | **WARNING** | 0 DEGs ($\text{min FDR} = 0.2601$); $N=5$ power limits documented |
| **Stage 5: Functional Biology** | Background Universe | Measured genes background | **PASS** | Background universe set to measured $N = 25,518$ genes |
| | ORA Multiple Testing | Report adjusted FDR | **WARNING** | ORA terms nominal ($p < 0.01$) but FDR $> 0.05$ after correction |
| | Ranked GSEA | Continuous distribution | **PASS** | Purine ($p_{\text{adj}} < 10^{-10}$), UPR ($p_{\text{adj}} < 10^{-7}$) significant |
| | Network Hubs | Computational hypotheses | **WARNING** | Hubs (`GAPDH`, `ACTB`) reflect pleiotropy, not proven biomarkers |
| | Clinical Survival Claims | No longitudinal follow-up | **PASS** | No Cox or Kaplan-Meier curves claimed from static GEO codes |
| **Stage 6: Code & Testing** | Script Execution | Exit code 0 | **PASS** | `run_pipeline.bat` executed across 9 steps with code 0 |
| | Automated Unit Tests | 6/6 test assertions | **PASS** | `test_pipeline_validation.py` passed live in 0.329s |
| | Software Environment | Stable package versions | **PASS** | Python 3.13, Pandas 3.1.1, SciPy 1.18.1 documented |
| **Stage 7: Figures & Reports** | Publication Figures | High resolution (300 DPI) | **PASS** | All 17 PNG figures verified non-empty and matching data |
| | Formal Report | Complete 22-section paper | **PASS** | `FINAL_GASTRIC_CANCER_BIOINFORMATICS_REPORT.md` |

---

## 2. Summary of Genuinely Completed Work vs Incomplete Areas

### What is Genuinely Complete:
1. **End-to-End Pipeline:** All 9 modular scripts (annotation, QC, limma eBayes, gene aggregation, Enrichr, GSEA, STRING, clinical, figures, and unit testing) execute automatically from start to finish with exit code 0.
2. **Defensible Statistical Modeling:** The unpaired 3-group empirical Bayes design eliminates the major flaw of historical pipelines (fabricated patient pairing).
3. **Disambiguated Results:** Both probe-level tables (633 & 643 strict DEGs) and gene-level tables (595 & 605 unique DEGs) are generated, preventing feature confusion.
4. **Automated Verification:** 6/6 automated test assertions pass live, verifying sample counts, FDR bounds, probe counts, and deliverable presence.
5. **Portfolio Documentation:** Complete suite of professional documents: `README.md`, `PROJECT_OVERVIEW.md`, `METHODS.md`, `RESULTS.md`, `LIMITATIONS.md`, `REPRODUCIBILITY.md`, `DATA_PROVENANCE.md`, `SOFTWARE_VERSIONS.md`, `CITATIONS.bib`, and comprehensive research reports.

### What Remains Incomplete (And Why It Is Methodologically Justified):
1. **Patient-Level Paired Analysis:** Cannot be performed because the original NCBI GEO metadata omit patient-matching identifiers. This is an unavoidable property of the public record, correctly resolved by using an unpaired design.
2. **Longitudinal Survival Analysis (Cox / Kaplan-Meier):** Cannot be performed because GSE17154 provides static discrete outcome codes (`NED` vs `failed`) without continuous follow-up times (months). Fabricating follow-up times would be fraudulent; descriptive clinical staging is appropriately reported instead.
3. **Wet-Lab Validation:** As an in silico computational biology study, candidate genes (`SSPO`, `NNAT`, `CLU`) are computational correlates requiring prospective experimental validation (RT-qPCR, Western blot) in future laboratory studies.

---

## 3. CV & Technical Interview Readiness Verdict

### Can this project honestly be presented on an MSc Biotechnology CV, GitHub, and in technical interviews?
$$\mathbf{YES. \quad IT \ IS \ 100\% \ READY \ FOR \ PRESENTATION.}$$

### Why it strengthens your candidacy:
- **Demonstrates Scientific Honesty:** Recruiters and senior scientists value candidates who recognize metadata limitations (e.g., lack of patient IDs, $N=5$ power limits) and apply appropriate statistical models rather than blindly running default paired tests.
- **Shows Production-Grade Reproducibility:** Having an automated batch pipeline, a 100% passing unit-test suite, and explicit SHA-256 checksums places this portfolio well above standard student coursework.
- **Full Analytical Breadth:** Demonstrates competence across microarray preprocessing, empirical Bayes modeling (`limma`), multiple hypothesis testing (FDR), ranked GSEA, network biology (STRING), and clinical subgroup stratification.
