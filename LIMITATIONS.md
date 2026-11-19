# SCIENTIFIC LIMITATIONS AND METHODOLOGICAL CAVEATS

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  

---

## 1. Technological Platform Constraints

- **Two-Colour Microarray Dynamic Range:** Agilent 4x44K arrays measure competitive hybridization fluorescence ratios against a common reference pool. Microarray technology has inherent background compression and fluorescence saturation ceilings compared to digital high-throughput RNA-sequencing (RNA-seq).

---

## 2. Statistical Power & Healthy Control Cohort Size

- **$N = 5$ in Apparently Normal Controls:** The healthy endoscopy control group comprises only 5 samples. Under an unpaired model with $N_1 = 20$ and $N_2 = 5$, statistical power is severely constrained after penalizing for 40,197 simultaneous tests.
- **Interpretation of `PN vs AN` (0 DEGs, min FDR = 0.2601):** Failure to reject the null hypothesis cannot be interpreted as proving biological identity between field mucosa and healthy mucosa. Subtle field cancerization alterations cannot be ruled out.

---

## 3. Absence of Longitudinal Clinical Follow-Up

- **No Survival Intervals:** The public NCBI GEO record provides static discrete outcome codes (`NED` vs `failed`) recorded at study submission. It lacks continuous overall survival (OS) or progression-free survival (PFS) follow-up times (months to event or right-censoring).
- **Prohibition of Survival Curves:** In strict adherence to scientific integrity, no Kaplan-Meier survival curves, log-rank tests, or Cox proportional hazards models were performed.

---

## 4. Translational Disclaimers

- **Computational Hypotheses vs Clinical Biomarkers:** All candidate genes and hub proteins identified herein represent statistical associations and in silico hypotheses derived from retrospective observational data. None are claimed to be clinically actionable diagnostic or prognostic biomarkers without prospective laboratory and multi-center clinical validation.
