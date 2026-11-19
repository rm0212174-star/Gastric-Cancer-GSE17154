@echo off
setlocal enabledelayedexpansion
echo ================================================================================
echo EXECUTING REAL GSE17154 GASTRIC CANCER BIOINFORMATICS PIPELINE
echo ================================================================================

echo [Step 1/9] Running Probe-to-Gene Annotation...
python build_probe_annotation.py
if %ERRORLEVEL% NEQ 0 ( echo Error in Step 1 & exit /b %ERRORLEVEL% )

echo [Step 2/9] Running Quality Control, Boxplots, Correlation and PCA...
python run_qc_and_annotation.py
if %ERRORLEVEL% NEQ 0 ( echo Error in Step 2 & exit /b %ERRORLEVEL% )

echo [Step 3/9] Running Limma Empirical Bayes Differential Expression Analysis...
python run_limma_deg.py
if %ERRORLEVEL% NEQ 0 ( echo Error in Step 3 & exit /b %ERRORLEVEL% )

echo [Step 4/9] Building Gene-Level Summarized DEG Tables...
python scripts\build_gene_level_degs.py
if %ERRORLEVEL% NEQ 0 ( echo Error in Step 4 & exit /b %ERRORLEVEL% )

echo [Step 5/9] Running Gene Ontology, KEGG, Reactome and GSEA Enrichment...
python scripts\run_enrichment.py
if %ERRORLEVEL% NEQ 0 ( echo Error in Step 5 & exit /b %ERRORLEVEL% )

echo [Step 6/9] Running Protein-Protein Interaction (STRING v12.5) Analysis...
python scripts\run_ppi_network.py
if %ERRORLEVEL% NEQ 0 ( echo Error in Step 6 & exit /b %ERRORLEVEL% )

echo [Step 7/9] Running Clinical Subgroup Analysis...
python scripts\run_clinical_analysis.py
if %ERRORLEVEL% NEQ 0 ( echo Error in Step 7 & exit /b %ERRORLEVEL% )

echo [Step 8/9] Generating Study Workflow Diagram and Publication Figures...
python scripts\generate_workflow_figure.py
if %ERRORLEVEL% NEQ 0 ( echo Error in Step 8 & exit /b %ERRORLEVEL% )

echo [Step 9/9] Running Automated Scientific Validation Test Suite...
python -m unittest tests\test_pipeline_validation.py
if %ERRORLEVEL% NEQ 0 ( echo Error in Step 9 - Validation Tests Failed & exit /b %ERRORLEVEL% )

echo ================================================================================
echo PIPELINE COMPLETED SUCCESSFULLY! All results, figures, and tests passed.
echo ================================================================================
