# DATA DOWNLOAD LOG & RETRIEVAL AUDIT

**Accession:** NCBI GEO GSE17154  
**Date of Retrieval:** 2026-11-19  
**Source Organization:** National Center for Biotechnology Information (NCBI) / European Bioinformatics Institute (EBI)  

---

## 1. Retrieved Artifacts & Integrity Verification

| Target File | Official Source URL | File Size | SHA-256 Checksum | Protocol / Tool | Verification Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GSE17154_series_matrix.txt.gz` | `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE17nnn/GSE17154/matrix/GSE17154_series_matrix.txt.gz` | 11,435,656 bytes | `8ddf0170a3cc7cf87fc1df37b31c1fe91cade401d3df55e329e8a2805a5f2b43` | HTTPS / Python `urllib` | Complete; 49 samples, 44,544 probes |
| `GPL6699_family.soft.gz` | `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL6nnn/GPL6699/soft/GPL6699_family.soft.gz` | 65,595,655 bytes | `1d723d5189cc1bfd5514a36e040642166b844ae6436a6138ef05ab98b45d4521` | HTTPS / Python `urllib` | Complete; 44,544 probe annotations |
| `GSM429115.gpr.gz` | `https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM429nnn/GSM429115/suppl/GSM429115.gpr.gz` | 3,694,047 bytes | `bce86dd31b4034d041be40b31f7a9319379baf2823c6fc7541b54bf0c2e23573` | HTTPS / Python `urllib` | Complete; raw GenePix 44,544 spots |
| `PMC3004887_publication.xml` | `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3004887/fullTextXML` | 125,914 bytes | `9ec1f9fdf00877a5efdf79e0a89d115ee8d98d89a26315ee409fcf1cfcf95d1d` | REST API | Complete publication XML |
| `PMID21092330_summary.json` | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=21092330&retmode=json` | 2,082 bytes | `0f0ebef4464ffc95029e0618018e69c0d60c29a2862e3c09b0235ddf905080e7` | Entrez E-Utilities | Bibliographic summary verified |

---

## 2. Preprocessing & Value Type Verification

- **Array Architecture:** Two-colour Agilent 4x44K spotted oligonucleotide array.
- **Dye Labeling:** Cy5 = patient specimen (tumor or normal mucosa); Cy3 = Stratagene Universal Human Reference RNA (UHRR).
- **Measurement Scale:** The series matrix `VALUE` field contains normalised $\log_2(\text{Cy5}/\text{Cy3})$ ratios.
- **Integrity Rule Applied:** No secondary $\log_2$ transformation was applied. No repeated normalization was performed.
