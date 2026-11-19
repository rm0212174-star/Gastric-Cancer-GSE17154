# PROTEIN-PROTEIN INTERACTION (PPI) NETWORK ANALYSIS REPORT (STAGE 7)

**Project Title:** Integrated Transcriptomic and Network-Based Analysis of Gastric Cancer Using GEO Dataset GSE17154  
**Date:** 2026-11-19  
**Database:** STRING v12.5 (*Homo sapiens*, Taxonomy ID: 9606)  
**Confidence Threshold:** Interaction Score $\ge 0.400$ (Medium Confidence)  

---

## 1. Network Topology & Graph Architecture

- **Total Query Nodes:** 45 top candidate differentially expressed transcripts.
- **Interacting Edges Identified:** Exactly **13 verified interaction edges**.
- **Connected Components:** The network partitions into a core interconnected multi-protein module centered on metabolic and structural regulators, with several isolated nodes.
- **Visualization:** [PPI_Network.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/PPI_Network.png) (and [PPI_Network_STRING.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/PPI_Network_STRING.png)).

---

## 2. Candidate Hub Genes & Graph Centrality Metrics

| Gene Symbol | Moderated Log2FC | Degree | Betweenness Centrality | Closeness Centrality | Functional Annotation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`GAPDH`** | -3.452 | **5** | 0.0412 | 0.1392 | Glycolytic cornerstone & moonlight nuclear regulator |
| **`ACTB`** | -3.384 | **5** | 0.0412 | 0.1392 | Cytoskeletal actin microfilament mediator |
| **`CSF3`** | -3.462 | **3** | 0.0155 | 0.1114 | Granulocyte colony-stimulating factor |
| **`LTF`** | -1.378 | **3** | 0.0082 | 0.1012 | Mucosal iron-binding antimicrobial glycoprotein |
| **`CTSD`** | -2.967 | **2** | 0.0000 | 0.0857 | Lysosomal aspartic protease mediating proteolysis |
| **`VDAC3`** | -2.699 | **2** | 0.0000 | 0.0857 | Mitochondrial voltage-dependent anion channel |
| **`GAD1`** | -1.800 | **2** | 0.0000 | 0.0857 | Glutamate decarboxylase 1 |
| **`OSMR`** | -2.617 | **1** | 0.0000 | 0.0696 | Oncostatin M cytokine receptor |

---

## 3. Methodological Caveats & Translational Warnings

> [!CAUTION]
> **Network Centrality Does Not Equate to Oncogenic Driving**  
> 1. Prominent hub nodes such as `GAPDH` and `ACTB` are highly connected primarily because they are ubiquitous structural and metabolic proteins with thousands of documented interactions in the literature.
> 2. Their high degree centrality reflects their pleiotropic cellular roles rather than cancer-specific causal oncogene status.
> 3. In strict compliance with research integrity standards, these hub genes are designated as **exploratory computational hypotheses**. None are claimed to be clinically actionable biomarkers without prospective mechanistic and functional laboratory validation.

---

## 4. Deliverables
- [STRING_INPUT_GENES.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/STRING_INPUT_GENES.csv)
- [STRING_NETWORK_EDGES.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/STRING_NETWORK_EDGES.csv)
- [PPI_HUB_GENES.csv](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/PPI_HUB_GENES.csv)
- [PPI_Network.png](file:///C:/Users/ACER/BIoinformatics_Training/12_Real_GSE17154_Analysis/figures/PPI_Network.png)
