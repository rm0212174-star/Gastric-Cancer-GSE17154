# BIOLOGICAL INTERPRETATION AND LITERATURE REVIEW REPORT (STAGE 9)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  

---

## 1. Deep Functional Characterization of Key Upregulated Transcripts

### 1.1 `SSPO` (SCO-Spondin / Spondin 1, $\log_2\text{FC} = +1.95$, $\text{FDR} = 3.25 \times 10^{-5}$)
- **Cellular Function:** High-molecular-weight extracellular matrix glycoprotein featuring multiple thrombospondin type 1 (TSR1) domains and von Willebrand factor type C (VWC) repeats.
- **Observed Direction:** Strongly elevated in gastric adenocarcinoma compared to both paired and healthy mucosa.
- **Biological Mechanism:** TSR1 domains interact directly with cell-surface proteoglycans, integrins, and latent $\text{TGF}-\beta$ complexes. In gastric cancer, desmoplastic stroma expansion and abnormal ECM remodeling are key drivers of local tissue invasion and chemoresistance.
- **Evidence Level:** Computational transcriptomic association from empirical microarray data; supported by literature on spondin family glycoproteins in tumor matrix stiffness.

### 1.2 `NNAT` (Neuronatin, $\log_2\text{FC} = +1.94$ in PN, $+2.74$ in AN, $\text{FDR} = 4.90 \times 10^{-5}$)
- **Cellular Function:** Endoplasmic reticulum proteolipid that modulates sarcoplasmic/endoplasmic reticulum calcium ATPase ($\text{SERCA}$) activity and governs intracellular calcium flux.
- **Observed Direction:** Dramatically upregulated in tumor tissue.
- **Biological Mechanism:** Perturbation of ER calcium signaling activates the Unfolded Protein Response (UPR) and stress kinase cascades. Our ranked GSEA independently detected significant activation of the UPR pathway ($p_{\text{adj}} = 2.09 \times 10^{-8}$). Elevated `NNAT` reflects adaptive neuroendocrine-like transdifferentiation and ER stress resilience enabling rapid tumor cell survival under hypoxic conditions.
- **Evidence Level:** Statistically verified computational finding; consistent with findings of altered calcium signaling in poorly differentiated gastric adenocarcinomas.

### 1.3 `CLU` (Clusterin, $\log_2\text{FC} = +1.44$, $\text{FDR} = 4.90 \times 10^{-5}$)
- **Cellular Function:** Heterodimeric secreted molecular chaperone that prevents protein aggregation and confers resistance to apoptotic stressors.
- **Observed Direction:** Elevated in gastric cancer specimens.
- **Biological Mechanism:** In response to cellular proteotoxic and hypoxic stress, secretory clusterin acts as an extracellular chaperone that stabilizes misfolded proteins, suppresses Bax-mediated mitochondrial apoptosis, and activates NF-$\kappa$B prosurvival signaling.
- **Evidence Level:** Well-documented in peer-reviewed oncology literature; observed as a statistical associate of malignant tissue in GSE17154.

---

## 2. Characterization of Key Repressed Transcripts

### 2.1 `ATP1B4` (ATPase $\text{Na}^+/\text{K}^+$ Transporting Beta 4, $\log_2\text{FC} = -4.31$, $\text{FDR} = 2.68 \times 10^{-11}$)
- **Cellular Function:** Transmembrane regulatory $\beta$-subunit of the P-type cation transport ATPase family.
- **Observed Direction:** The most statistically significant down-regulated transcript in the entire dataset.
- **Biological Mechanism:** Mature gastric epithelial cells (parietal and chief cells) maintain specialized electrogenic ion transport machinery to support gastric acid secretion and mucosal homeostasis. Profound loss of `ATP1B4` reflects terminal epithelial dedifferentiation and loss of apical-basal polarity during gastric malignant transformation.
- **Evidence Level:** Empirical transcriptomic observation; represents cellular dedifferentiation.

### 2.2 `KLRA1` (Killer Cell Lectin-Like Receptor A1, $\log_2\text{FC} = -4.29$, $\text{FDR} = 1.29 \times 10^{-10}$)
- **Cellular Function:** C-type lectin-like inhibitory receptor expressed on natural killer (NK) cells and cytotoxic T-cell subsets.
- **Observed Direction:** Strongly decreased in tumor biopsies.
- **Biological Mechanism:** In tumor tissue, decreased detection reflects both the dilution of normal resident immune cell populations by expanding cancer epithelial cells and local immunosuppression / immune cell exclusion in the tumor microenvironment.

---

## 3. Dissecting the Coordinated Pathway Architecture

1. **Purine Metabolism ($p_{\text{adj}} = 3.52 \times 10^{-11}$):**
   - Rapidly proliferating cancer cells require elevated purine nucleotide pools for DNA synthesis, RNA transcription, and ATP generation. Upregulation of purine biosynthetic enzymes is a classic hallmark of gastric cancer metabolic rewiring.
2. **Glycolysis / Gluconeogenesis ($p_{\text{adj}} = 6.18 \times 10^{-8}$):**
   - Represents the Warburg effect, where gastric tumor cells preferentially rely on aerobic glycolysis for energy and biosynthetic precursors.
3. **Unfolded Protein Response (UPR, $p_{\text{adj}} = 2.09 \times 10^{-8}$):**
   - High translation rates in neoplastic cells induce ER proteotoxic stress. UPR induction allows tumor cells to survive hostile microenvironmental conditions.
4. **JAK-STAT Signaling Pathway ($p_{\text{adj}} = 4.09 \times 10^{-7}$):**
   - Mediates cytokine and growth factor signaling from the inflammatory gastric stroma, promoting cell survival, migration, and immune evasion.

---

## 4. Distinction Between Association and Causation

> [!IMPORTANT]
> All differential expression results documented herein represent **statistical associations** derived from retrospective observational microarray transcriptomic data. While biologically plausible mechanisms link these genes to gastric carcinogenesis, observational transcriptomic data cannot prove causal etiology. No candidate gene is claimed to be an established therapeutic target or diagnostic biomarker without prospective experimental knockdown/overexpression assays and multi-center clinical trials.
