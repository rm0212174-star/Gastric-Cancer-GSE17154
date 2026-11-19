# INITIAL AUDIT EXECUTION AND FORENSIC VERIFICATION RESULTS

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date of Audit:** 2026-11-19  
**Workspace Audited:** `C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis`  
**Backup Location:** `C:\Users\ACER\Bioinformatics_Training\01_Original_Backups\12_Real_GSE17154_Analysis_Backup_20261119`  
**Lead Auditor:** Senior Bioinformatics Scientist & Research Project Auditor  

---

## 1. Summary of `PROJECT_BACKUP_REPORT.md`

The pre-execution backup and forensic inventory report ([`PROJECT_BACKUP_REPORT.md`](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/reports/PROJECT_BACKUP_REPORT.md)) confirms:
- **Backup Verification:** A full, recursive, byte-for-byte copy of `12_Real_GSE17154_Analysis` was created in `01_Original_Backups/12_Real_GSE17154_Analysis_Backup_20261119` prior to analysis.
- **Historical Phase Isolation:** All historical training phases (`01_Original_Backups`, `02_Phase_1_Python_GEO` through `10_Final_Portfolio`) are strictly preserved and untouched.
- **Forensic File Inventory:** 138 total files were cataloged into `PROJECT_FILE_INVENTORY.csv` and `PROJECT_SHA256_CHECKSUMS.csv`, establishing baseline hashes for raw downloads, processed matrices, scripts, figures, and reports.

---

## 2. Verification of `GEO_DATA_VALIDATION_REPORT.md` Against Actual Downloaded Files

The claims in [`GEO_DATA_VALIDATION_REPORT.md`](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/reports/GEO_DATA_VALIDATION_REPORT.md) were independently tested against the physical files on disk:

| Target File | Expected Size (Report) | Actual Size on Disk | Expected SHA-256 Checksum | Actual Computed SHA-256 Checksum | Verification Result |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **`GSE17154_series_matrix.txt.gz`** | 11,435,656 bytes | 11,435,656 bytes | `8ddf0170a3cc7cf87fc1df37b31c1fe91cade401d3df55e329e8a2805a5f2b43` | `8ddf0170a3cc7cf87fc1df37b31c1fe91cade401d3df55e329e8a2805a5f2b43` | **EXACT MATCH** |
| **`GPL6699_family.soft.gz`** | 65,595,655 bytes | 65,595,655 bytes | `1d723d5189cc1bfd5514a36e040642166b844ae6436a6138ef05ab98b45d4521` | `1d723d5189cc1bfd5514a36e040642166b844ae6436a6138ef05ab98b45d4521` | **EXACT MATCH** |
| **`GSM429115.gpr.gz`** | 3,694,047 bytes | 3,694,047 bytes | `bce86dd31b4034d041be40b31f7a9319379baf2823c6fc7541b54bf0c2e23573` | `bce86dd31b4034d041be40b31f7a9319379baf2823c6fc7541b54bf0c2e23573` | **EXACT MATCH** |
| **`PMC3004887_publication.xml`** | 125,914 bytes | 125,914 bytes | `be04af5b547259ce5581996ea1ec5131c79a1ca375c39be0188a601a9e312098` | `be04af5b547259ce5581996ea1ec5131c79a1ca375c39be0188a601a9e312098` | **EXACT MATCH** |
| **`PMID21092330_summary.json`** | 2,082 bytes | 2,082 bytes | `9cd293be8a63fa591d47783813917b8826fb225ae9373efe12359b8c3edb4741` | `9cd293be8a63fa591d47783813917b8826fb225ae9373efe12359b8c3edb4741` | **EXACT MATCH** |

**Empirical Properties Confirmed:**
- The Series Matrix table header begins at `!series_matrix_table_begin` and contains exactly 44,544 rows and 49 columns.
- The `VALUE` measurements represent normalized $\log_2(\text{Cy5}/\text{Cy3})$ ratios against Stratagene Universal Human Reference RNA (UHRR).
- Only 1 missing entry exists in the entire dataset (Probe ID `24` in sample `GSM429144`), which is imputed using the probe-level mean ($\mu = -0.0497$).

---

## 3. Review of `SAMPLE_GROUP_VALIDATION_REPORT.md` & `EXPERIMENTAL_DESIGN_REPORT.md`

### 3.1 Sample Cohort Structure
- **Gastric Cancer (`CANCER`, $N = 24$):** 23 adenocarcinomas, 1 neuroendocrine carcinoma.
- **Paired Normal (`Paired_Normal_PN`, $N = 20$):** Biopsies of non-malignant mucosa from the **same stomach** as cancer patients, confirmed free of microscopic tumors by frozen section.
- **Apparently Normal (`Apparently_Normal_AN`, $N = 5$):** Gastric mucosa from healthy endoscopy volunteers.

### 3.2 Statistical Pairing vs Biological Tissue Origin
1. **No 1-to-1 Patient Identifiers:** In the public GEO record, all sample descriptions state `'no additional information'`. There are no hospital IDs or pair tags linking `CANCER - X` to `PN - Y`.
2. **Asymmetrical Sample Sizes:** $N_{\text{Cancer}} = 24 \neq N_{\text{PN}} = 20$. Exactly 4 cancer samples have no corresponding normal mucosa.
3. **Statistical Resolution:** Attempting a paired $t$-test or blocked model (`~ Patient + Tissue`) would require fabricating 20 synthetic pairings and discarding 4 cancer samples. In accordance with the original publication (Rajkumar *et al.*, 2010), which utilized an unpaired random-variance $F$-test in BRB-ArrayTools, an **unpaired 3-group linear model** (`~ 0 + Group`) is applied. The label `Paired_Normal_PN` strictly reflects biological provenance, not statistical pairing.

---

## 4. Automated Validation Test Suite: Code, Logic & Execution

### 4.1 Test Code Structure (`tests/test_pipeline_validation.py`)
The suite implements 6 independent assertion methods using Python's `unittest` framework:
1. `test_01_sample_metadata_counts`: Asserts that `FINAL_SAMPLE_METADATA.csv` has 49 rows, 49 unique IDs, 24 CANCER, 20 PN, and 5 AN.
2. `test_02_probe_annotation_and_filtering`: Asserts 44,544 total probes, 4,347 control probes (`Is_Control == True`), 40,197 experimental probes, and 25,518 unique gene symbols.
3. `test_03_deg_statistical_validity`: Asserts that all 40,197 experimental probes have $0.0 \le \text{FDR} \le 1.0$ and finite $\log_2\text{FC}$ across all 3 contrasts.
4. `test_04_deg_strict_counts_reproducibility`: Asserts exact probe-level (633 & 643) and gene-level (595 & 605) counts.
5. `test_05_pn_vs_an_no_false_positives`: Asserts that `PN vs AN` yields 0 DEGs at FDR < 0.05, with minimum FDR matching $\approx 0.2601$.
6. `test_06_required_output_files_exist_and_nonempty`: Asserts that all 17 required publication figures and result tables exist and are non-empty.

### 4.2 Live Test Execution Evidence
- **Exact Command Executed:**
  ```cmd
  python -m unittest -v "c:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis\tests\test_pipeline_validation.py"
  ```
- **Exit Code:** `0`
- **Warnings:** `0`
- **Execution Output:**
  ```
  test_01_sample_metadata_counts (12_Real_GSE17154_Analysis.tests.test_pipeline_validation.TestGSE17154Pipeline.test_01_sample_metadata_counts)
  Test that exactly 49 samples exist with expected group partitions. ... ok
  test_02_probe_annotation_and_filtering (12_Real_GSE17154_Analysis.tests.test_pipeline_validation.TestGSE17154Pipeline.test_02_probe_annotation_and_filtering)
  Test probe filtering: 44,544 total, 4,347 controls, 40,197 experimental. ... ok
  test_03_deg_statistical_validity (12_Real_GSE17154_Analysis.tests.test_pipeline_validation.TestGSE17154Pipeline.test_03_deg_statistical_validity)
  Test FDR bounds (0 <= FDR <= 1) and finite log2 fold changes in full DEG tables. ... ok
  test_04_deg_strict_counts_reproducibility (12_Real_GSE17154_Analysis.tests.test_pipeline_validation.TestGSE17154Pipeline.test_04_deg_strict_counts_reproducibility)
  Verify exact probe-level and gene-level DEG counts. ... ok
  test_05_pn_vs_an_no_false_positives (12_Real_GSE17154_Analysis.tests.test_pipeline_validation.TestGSE17154Pipeline.test_05_pn_vs_an_no_false_positives)
  Verify that PN vs AN yields 0 DEGs at FDR < 0.05 (minimum FDR is ~0.2601). ... ok
  test_06_required_output_files_exist_and_nonempty (12_Real_GSE17154_Analysis.tests.test_pipeline_validation.TestGSE17154Pipeline.test_06_required_output_files_exist_and_nonempty)
  Verify all critical output figures, reports, and tables exist and are non-empty. ... ok

  ----------------------------------------------------------------------
  Ran 6 tests in 0.250s

  OK
  ```
- **Summary:**
  - Total Tests: **6**
  - Passed Tests: **6**
  - Failed Tests: **0**
  - Errors: **0**

---

## 5. Verification of Input Data, Feature Dimensions, and Outputs

### 5.1 Dimensional Verification
- **Total Array Probes (GPL6699):** 44,544
- **Technical Control Spots:** 4,347 (flagged via Agilent control spot IDs and negative control prefixes)
- **Experimental Probes:** 40,197 (100% mapped to Gene Symbols)
- **Unique Human Genes:** 25,518
- **Single-Probe Genes:** 18,174
- **Multi-Probe Genes:** 7,344 (e.g., `ACTB` has 392 probes; housekeeping controls have 104 probes)

### 5.2 Verification of Result CSV Tables
All result tables were confirmed to derive directly from empirical data:
- `DEG_Cancer_vs_PN_Full.csv`: 40,197 probes ranked.
- `DEG_Cancer_vs_PN_Top_FDR05_FC2.csv`: Exactly 633 strict probes (60 Up, 573 Down).
- `DEG_Cancer_vs_PN_Gene_Level_Strict_FDR05_FC2.csv`: Exactly 595 unique genes (52 Up, 543 Down).
- `DEG_Cancer_vs_AN_Full.csv`: 40,197 probes ranked.
- `DEG_Cancer_vs_AN_Top_FDR05_FC2.csv`: Exactly 643 strict probes (93 Up, 550 Down).
- `DEG_Cancer_vs_AN_Gene_Level_Strict_FDR05_FC2.csv`: Exactly 605 unique genes (81 Up, 524 Down).
- `DEG_PN_vs_AN_Full.csv`: 40,197 probes ranked.
- `DEG_PN_vs_AN_Top_FDR05_FC2.csv`: Exactly 0 rows (minimum FDR = 0.2601).
- `DEG_PN_vs_AN_Gene_Level_Strict_FDR05_FC2.csv`: Exactly 0 rows.

---

## 6. Audit of Simulated, Duplicate, or Conflicting Results

1. **Simulated / Synthetic Data Audit:**
   - A global text search across all scripts in `12_Real_GSE17154_Analysis` confirmed **zero occurrences of simulated, synthetic, or mock data generation**.
   - All references to "synthetic" in reports explicitly document the *rejection* of synthetic pairing and the *isolation* of historical training simulations.
2. **Duplicate Files:**
   - Root-level vs subdirectory copies: Result CSVs and PNGs were synchronized between root `12_Real_GSE17154_Analysis/` and subdirectories (`results/`, `figures/`) to ensure full backwards compatibility with legacy scripts while maintaining a clean hierarchical structure.
3. **Experimental Design Consistency:**
   - No scripts or reports claim a matched-pair $t$-test.
   - All models parameterize the unpaired formula `~ 0 + Group`.
   - No clinical survival curves (Kaplan-Meier/Cox) are claimed.

---

## 7. Audit Verdict & Synthesis

### Verified Findings
1. All 49 samples and 44,544 probes are authentic, unmodified data from NCBI GEO GSE17154 and GPL6699.
2. The empirical Bayes `limma` model correctly implements an unpaired 3-group design.
3. Probe counts (633 and 643 strict probes) and unique gene counts (595 and 605 strict genes) are fully disambiguated.
4. The absence of DEGs in `PN vs AN` (min FDR = 0.2601) is correctly documented as constrained by the sample size ($N = 5$ in AN), avoiding false claims of biological equivalence.
5. All 6 automated validation tests execute live and pass with Exit Code 0 in 0.250s.
6. The entire 9-step batch pipeline (`run_pipeline.bat`) runs end-to-end with Exit Code 0.

### Unverified Claims
- None. All numerical claims in reports and summaries match the physical CSV tables and test assertions.

### Failed Tests
- **0 tests failed.** (6 passed, 0 failures, 0 errors).

### Missing Files
- **0 missing files.** All 17 required publication figures, tables, logs, metadata, and reports are present and non-empty.

### Scientific Concerns Documented
1. **Dynamic Range:** Microarrays exhibit fluorescence saturation ceilings and compression compared to RNA-seq.
2. **Statistical Power for AN:** With only $N = 5$ healthy endoscopic controls, subtle field cancerization changes cannot be detected under strict FDR correction.
3. **No Survival Follow-up:** GSE17154 lacks longitudinal time-to-event follow-up intervals, precluding Cox modeling.
4. **Hub Proteins as Hypotheses:** Prominent hubs (`GAPDH`, `ACTB`) reflect pleiotropic connectivity rather than validated clinical biomarkers.

### Recommended Next Steps
1. The project has satisfied all auditing criteria and holds the official status **`VERIFIED WITH DOCUMENTED LIMITATIONS`**.
2. Proceed to review the finalized deliverables in [`FINAL_GASTRIC_CANCER_BIOINFORMATICS_REPORT.md`](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/reports/FINAL_GASTRIC_CANCER_BIOINFORMATICS_REPORT.md).
3. The project is fully ready for inclusion in the student's MSc Biotechnology portfolio, research presentations, and technical interviews.
