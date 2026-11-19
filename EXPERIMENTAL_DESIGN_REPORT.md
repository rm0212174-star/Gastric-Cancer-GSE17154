# EXPERIMENTAL DESIGN REPORT (STAGE 2)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  

---

## 1. Experimental Design Overview

```
                      [GSE17154 Clinical Cohort (N = 49)]
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
  Gastric Cancer                Paired Normal              Apparently Normal
    (CANCER)                  (Paired_Normal_PN)          (Apparently_Normal_AN)
     N = 24                        N = 20                        N = 5
         │                            │                            │
         └─────────────┬──────────────┴──────────────┬─────────────┘
                       ▼                             ▼
              Contrast A: Cancer vs PN      Contrast B: Cancer vs AN
                       │                             │
                       └──────────────┬──────────────┘
                                      ▼
                             Contrast C: PN vs AN
```

---

## 2. Microarray Chemistry & Normalization Framework

- **Technology:** Agilent 4x44K two-colour spotted 60-mer oligonucleotide arrays (GPL6699).
- **Hybridization Scheme:** Common reference design.
  - Test Channel (Cy5 / Red): Experimental specimen total RNA (24 Cancer, 20 PN, 5 AN).
  - Reference Channel (Cy3 / Green): Stratagene Universal Human Reference RNA (UHRR).
- **Processed Metric:** The reported expression value for spot $i$ in array $j$ is:
  $$\text{VALUE}_{ij} = \log_2\left(\frac{\text{Cy5}_{ij}}{\text{Cy3}_{ij}}\right) - \text{Median}\left[\log_2\left(\frac{\text{Cy5}}{\text{Cy3}}\right)_j\right]$$
- **Linear Modeling Formulation:** Because all samples were competitively hybridized against an identical common reference pool, the individual log-ratio values are directly comparable across arrays. The linear model is parameterized in `limma`:
  $$Y_{gi} = \beta_{g,\text{Cancer}} \cdot X_{i,\text{Cancer}} + \beta_{g,\text{PN}} \cdot X_{i,\text{PN}} + \beta_{g,\text{AN}} \cdot X_{i,\text{AN}} + \varepsilon_{gi}$$
  where $\varepsilon_{gi} \sim \mathcal{N}(0, \sigma_g^2)$ with empirical Bayes shrinkage of gene-specific variances toward a common prior.
