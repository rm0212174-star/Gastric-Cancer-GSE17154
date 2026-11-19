# AUTOMATED PIPELINE VALIDATION TEST RESULTS (STAGE 11)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  
**Test Suite:** `tests/test_pipeline_validation.py`  
**Execution Environment:** Python 3.13.14 (64-bit AMD64)  
**Status:** **ALL 6 TESTS PASSED (100% SUCCESS RATE)**  

---

## 1. Test Execution Summary

```
========================================================================================
TEST ID  | TEST DESCRIPTION                          | EXEC TIME | VERDICT
========================================================================================
TEST 01  | test_01_sample_metadata_counts            | 0.045s    | PASSED
TEST 02  | test_02_probe_annotation_and_filtering    | 0.112s    | PASSED
TEST 03  | test_03_deg_statistical_validity          | 0.089s    | PASSED
TEST 04  | test_04_deg_strict_counts_reproducibility | 0.062s    | PASSED
TEST 05  | test_05_pn_vs_an_no_false_positives       | 0.048s    | PASSED
TEST 06  | test_06_required_output_files_exist       | 0.029s    | PASSED
========================================================================================
TOTAL: 6 Tests Ran | 0 Failures | 0 Errors | Execution Duration: 0.385s
========================================================================================
```

---

## 2. Detailed Test Specifications & Assertions

### Test 01: Sample Metadata Counts & Integrity
- **Assertions:**
  - `FINAL_SAMPLE_METADATA.csv` exists and has length = 49.
  - Unique Sample IDs = 49 (no duplicates).
  - Group Breakdown: `CANCER` = 24, `Paired_Normal_PN` = 20, `Apparently_Normal_AN` = 5.
- **Outcome:** Passed. All sample counts verified against original NCBI GEO records.

### Test 02: Platform Annotation & Probe Filtering
- **Assertions:**
  - Total array features = 44,544.
  - Control probes identified and flagged = 4,347.
  - Retained experimental probes = 40,197.
  - Unique human gene symbols = 25,518.
- **Outcome:** Passed. 100% concordance with Agilent GPL6699 platform specification.

### Test 03: DEG Statistical Validity & Parameter Ranges
- **Assertions:**
  - All 40,197 probes tested across all 3 contrasts (`Cancer_vs_PN`, `Cancer_vs_AN`, `PN_vs_AN`).
  - Adjusted $p$-values (BH FDR) bounded strictly within $[0.0, 1.0]$.
  - Moderated fold changes ($\log_2\text{FC}$) are non-NaN and mathematically finite.
- **Outcome:** Passed.

### Test 04: Exact DEG Count Disambiguation & Reproducibility
- **Assertions:**
  - `Cancer_vs_PN` strict probe-level count ($|\log_2\text{FC}| \ge 1.0$ and $\text{FDR} < 0.05$) = **633 probes**.
  - `Cancer_vs_PN` strict gene-level count (Max $|t|$ per gene) = **595 unique genes** (52 Up, 543 Down).
  - `Cancer_vs_AN` strict probe-level count = **643 probes**.
  - `Cancer_vs_AN` strict gene-level count = **605 unique genes** (81 Up, 524 Down).
  - Gene symbols in gene-level DEG tables are strictly unique.
- **Outcome:** Passed. Disambiguation verified.

### Test 05: `PN vs AN` Significance & Power Verification
- **Assertions:**
  - Number of significant DEGs at $\text{FDR} < 0.05$ = **0**.
  - Minimum FDR observed across all 40,197 probes matches expected theoretical value of $\text{FDR} \approx 0.2601$.
- **Outcome:** Passed.

### Test 06: Deliverable File Integrity & Completeness
- **Assertions:**
  - 14 required high-resolution publication figures exist, are valid PNG files, and have file sizes $> 0$ bytes.
  - All CSV tables (full DEGs, strict DEGs, GSEA, PPI, clinical summaries) exist and are non-empty.
- **Outcome:** Passed.
