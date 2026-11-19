# DATA PROVENANCE AND AUTHENTICITY SPECIFICATION

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  

---

## 1. Primary Public Sources & Verified Accessions

All primary data were retrieved exclusively from official National Center for Biotechnology Information (NCBI) repositories:

| Resource Accession | Description | Official URL | File Size | Verified SHA-256 Checksum |
| :--- | :--- | :--- | :---: | :--- |
| **NCBI GEO GSE17154** | Series Matrix table (44,544 probes $\times$ 49 samples) | `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE17nnn/GSE17154/matrix/GSE17154_series_matrix.txt.gz` | 11.4 MB | `8ddf0170a3cc7cf87fc1df37b31c1fe91cade401d3df55e329e8a2805a5f2b43` |
| **NCBI GEO GPL6699** | Platform annotation table (Agilent 4x44K G4112F) | `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL6nnn/GPL6699/soft/GPL6699_family.soft.gz` | 65.6 MB | `1d723d5189cc1bfd5514a36e040642166b844ae6436a6138ef05ab98b45d4521` |
| **NCBI GEO GSM429115** | Sample CANCER-1 GenePix Results (GPR) raw file | `https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM429nnn/GSM429115/suppl/GSM429115.gpr.gz` | 3.7 MB | `bce86dd31b4034d041be40b31f7a9319379baf2823c6fc7541b54bf0c2e23573` |
| **PubMed Central PMC3004887** | Full-text publication XML (Rajkumar et al., 2010) | `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3004887/fullTextXML` | 125.9 KB | `be04af5b547259ce5581996ea1ec5131c79a1ca375c39be0188a601a9e312098` |

---

## 2. Authenticity Guarantee

- **Zero Synthetic Replacements:** The expression values analyzed throughout this project originate 100% from empirical measurements in `GSE17154_series_matrix.txt.gz`.
- **Isolation of Historical Training Data:** Historical synthetic/mock matrices from prior training phases remain completely isolated in their original directories.
