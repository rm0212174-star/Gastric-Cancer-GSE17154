#!/usr/bin/env bash
set -e

echo "================================================================================"
echo "EXECUTING REAL GSE17154 GASTRIC CANCER BIOINFORMATICS PIPELINE"
echo "================================================================================"

echo "[Step 1/9] Running Probe-to-Gene Annotation..."
python3 build_probe_annotation.py

echo "[Step 2/9] Running Quality Control, Boxplots, Correlation and PCA..."
python3 run_qc_and_annotation.py

echo "[Step 3/9] Running Limma Empirical Bayes Differential Expression Analysis..."
python3 run_limma_deg.py

echo "[Step 4/9] Building Gene-Level Summarized DEG Tables..."
python3 scripts/build_gene_level_degs.py

echo "[Step 5/9] Running Gene Ontology, KEGG, Reactome and GSEA Enrichment..."
python3 scripts/run_enrichment.py

echo "[Step 6/9] Running Protein-Protein Interaction (STRING v12.5) Analysis..."
python3 scripts/run_ppi_network.py

echo "[Step 7/9] Running Clinical Subgroup Analysis..."
python3 scripts/run_clinical_analysis.py

echo "[Step 8/9] Generating Study Workflow Diagram & Publication Figures..."
python3 scripts/generate_workflow_figure.py

echo "[Step 9/9] Running Automated Scientific Validation Test Suite..."
python3 -m unittest tests/test_pipeline_validation.py

echo "================================================================================"
echo "PIPELINE COMPLETED SUCCESSFULLY! All results, figures, and tests passed."
echo "================================================================================"
