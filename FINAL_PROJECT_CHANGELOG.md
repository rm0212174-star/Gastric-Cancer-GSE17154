# PROJECT CHANGELOG & AUDIT TRAIL

All modifications, verifications, script executions, and corrections performed during the Gastric Cancer Bioinformatics Project lifecycle are documented below.

---

### [2026-11-19 22:56] - Stage 0: Backup and Forensic Inventory
- **Action:** Created complete timestamped backup of `12_Real_GSE17154_Analysis` into `01_Original_Backups/12_Real_GSE17154_Analysis_Backup_20261119`.
- **Script:** Created and executed `scripts/stage0_inventory_and_checksums.py`.
- **Deliverables:** Generated `PROJECT_FILE_INVENTORY.csv`, `PROJECT_SHA256_CHECKSUMS.csv`, and `reports/PROJECT_BACKUP_REPORT.md`.
- **Finding:** 138 files inventoried; SHA-256 signatures cataloged; zero data loss.

### [2026-11-19 22:43] - Stage 11: Reproducibility Verification
- **Action:** Executed `run_pipeline.bat` across all 8 modular pipeline steps.
- **Finding:** All 8 scripts exited with code 0.
- **Output:** QC plots, Limma DEG tables, Gene-level aggregation, Enrichr/GSEA, STRING PPI, Clinical analysis, and study workflow diagram generated.

### [2026-11-19 22:30] - Stage 3 & 5: Disambiguation of Probes vs Unique Genes
- **Action:** Added `scripts/build_gene_level_degs.py` to aggregate 40,197 experimental probes to 25,518 unique gene symbols using maximum absolute moderated $t$-statistic.
- **Outcome:** Correctly disambiguated probe DEGs (Cancer vs PN: 633 probes; Cancer vs AN: 643 probes) from unique gene DEGs (Cancer vs PN: 595 genes; Cancer vs AN: 605 genes).

### [2026-11-19 22:15] - Stage 1 & 2: Statistical Design Correction
- **Action:** Removed erroneous matched-pair modeling claims.
- **Outcome:** Implemented unpaired 3-group design (`~ 0 + Group`) in `limma` to match official GEO metadata where patient identifiers were unavailable. Renamed group identifiers to `CANCER`, `Paired_Normal_PN`, and `Apparently_Normal_AN`.
