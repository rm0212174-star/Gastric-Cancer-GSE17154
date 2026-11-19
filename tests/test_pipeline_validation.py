import os
import unittest
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestGSE17154Pipeline(unittest.TestCase):

    def setUp(self):
        self.base_dir = BASE_DIR
        self.meta_path = os.path.join(self.base_dir, "FINAL_SAMPLE_METADATA.csv")
        self.annot_path = os.path.join(self.base_dir, "data", "annotation", "Probe_Annotation.csv")
        self.deg_full_pn = os.path.join(self.base_dir, "results", "DEG", "DEG_Cancer_vs_PN_Full.csv")
        self.deg_strict_pn = os.path.join(self.base_dir, "results", "DEG", "DEG_Cancer_vs_PN_Top_FDR05_FC2.csv")
        self.gene_strict_pn = os.path.join(self.base_dir, "results", "DEG", "DEG_Cancer_vs_PN_Gene_Level_Strict_FDR05_FC2.csv")
        self.deg_full_an = os.path.join(self.base_dir, "results", "DEG", "DEG_Cancer_vs_AN_Full.csv")
        self.deg_strict_an = os.path.join(self.base_dir, "results", "DEG", "DEG_Cancer_vs_AN_Top_FDR05_FC2.csv")
        self.gene_strict_an = os.path.join(self.base_dir, "results", "DEG", "DEG_Cancer_vs_AN_Gene_Level_Strict_FDR05_FC2.csv")
        self.deg_full_pn_an = os.path.join(self.base_dir, "results", "DEG", "DEG_PN_vs_AN_Full.csv")

    def test_01_sample_metadata_counts(self):
        """Test that exactly 49 samples exist with expected group partitions."""
        self.assertTrue(os.path.exists(self.meta_path), "FINAL_SAMPLE_METADATA.csv missing")
        df = pd.read_csv(self.meta_path)
        self.assertEqual(len(df), 49, "Total sample count must be exactly 49")
        self.assertEqual(df["Sample_ID"].nunique(), 49, "Sample IDs must be unique")
        
        counts = df["Statistical_Group"].value_counts().to_dict()
        self.assertEqual(counts.get("CANCER", 0), 24, "Cancer sample count must be 24")
        self.assertEqual(counts.get("Paired_Normal_PN", 0), 20, "Paired Normal sample count must be 20")
        self.assertEqual(counts.get("Apparently_Normal_AN", 0), 5, "Apparently Normal sample count must be 5")

    def test_02_probe_annotation_and_filtering(self):
        """Test probe filtering: 44,544 total, 4,347 controls, 40,197 experimental."""
        self.assertTrue(os.path.exists(self.annot_path), "Probe_Annotation.csv missing")
        df = pd.read_csv(self.annot_path)
        self.assertEqual(len(df), 44544, "Total array spots must be 44,544")
        
        controls = df["Is_Control"].sum()
        self.assertEqual(controls, 4347, "Control probes must be exactly 4,347")
        
        exp_probes = len(df) - controls
        self.assertEqual(exp_probes, 40197, "Experimental probes must be exactly 40,197")
        
        # Test unique genes
        exp_df = df[~df["Is_Control"]]
        unique_genes = exp_df["Gene_Symbol"].nunique()
        self.assertEqual(unique_genes, 25518, "Unique human gene symbols must be exactly 25,518")

    def test_03_deg_statistical_validity(self):
        """Test FDR bounds (0 <= FDR <= 1) and finite log2 fold changes in full DEG tables."""
        for path in [self.deg_full_pn, self.deg_full_an, self.deg_full_pn_an]:
            self.assertTrue(os.path.exists(path), f"DEG table missing: {path}")
            df = pd.read_csv(path)
            self.assertEqual(len(df), 40197, f"All 40,197 experimental probes must be tested in {path}")
            
            # Check FDR range
            self.assertTrue((df["Adj_P_Value"] >= 0.0).all(), "FDR must be >= 0")
            self.assertTrue((df["Adj_P_Value"] <= 1.0).all(), "FDR must be <= 1")
            
            # Check finite log2FC
            self.assertFalse(df["Log2FC"].isna().any(), "Log2FC cannot have NaN")
            self.assertTrue(np.isfinite(df["Log2FC"]).all(), "Log2FC must be finite")

    def test_04_deg_strict_counts_reproducibility(self):
        """Verify exact probe-level and gene-level DEG counts."""
        # Probe-level Cancer vs PN: 633 probes
        df_p_pn = pd.read_csv(self.deg_strict_pn)
        self.assertEqual(len(df_p_pn), 633, "Cancer vs PN strict probe count must be exactly 633")
        
        # Gene-level Cancer vs PN: 595 unique genes
        df_g_pn = pd.read_csv(self.gene_strict_pn)
        self.assertEqual(len(df_g_pn), 595, "Cancer vs PN strict gene count must be exactly 595")
        self.assertEqual(df_g_pn["Gene_Symbol"].nunique(), 595, "Gene symbols in gene-level DEG must be unique")
        
        # Probe-level Cancer vs AN: 643 probes
        df_p_an = pd.read_csv(self.deg_strict_an)
        self.assertEqual(len(df_p_an), 643, "Cancer vs AN strict probe count must be exactly 643")
        
        # Gene-level Cancer vs AN: 605 unique genes
        df_g_an = pd.read_csv(self.gene_strict_an)
        self.assertEqual(len(df_g_an), 605, "Cancer vs AN strict gene count must be exactly 605")
        self.assertEqual(df_g_an["Gene_Symbol"].nunique(), 605, "Gene symbols in gene-level DEG must be unique")

    def test_05_pn_vs_an_no_false_positives(self):
        """Verify that PN vs AN yields 0 DEGs at FDR < 0.05 (minimum FDR is ~0.2601)."""
        df_pn_an = pd.read_csv(self.deg_full_pn_an)
        sig_count = (df_pn_an["Adj_P_Value"] < 0.05).sum()
        self.assertEqual(sig_count, 0, "PN vs AN must yield 0 significant DEGs at FDR < 0.05")
        min_fdr = df_pn_an["Adj_P_Value"].min()
        self.assertAlmostEqual(min_fdr, 0.2601, places=3, msg="Minimum FDR for PN vs AN must match ~0.2601")

    def test_06_required_output_files_exist_and_nonempty(self):
        """Verify all critical output figures, reports, and tables exist and are non-empty."""
        required_files = [
            # Figures
            os.path.join(self.base_dir, "figures", "QC_Boxplots.png"),
            os.path.join(self.base_dir, "figures", "QC_Density_Plots.png"),
            os.path.join(self.base_dir, "figures", "Sample_Correlation_Heatmap.png"),
            os.path.join(self.base_dir, "figures", "Sample_Clustering.png"),
            os.path.join(self.base_dir, "figures", "Real_Data_PCA.png"),
            os.path.join(self.base_dir, "figures", "Volcano_Cancer_vs_PN.png"),
            os.path.join(self.base_dir, "figures", "Volcano_Cancer_vs_AN.png"),
            os.path.join(self.base_dir, "figures", "Volcano_PN_vs_AN.png"),
            os.path.join(self.base_dir, "figures", "Heatmap_Top50_Cancer_vs_PN.png"),
            os.path.join(self.base_dir, "figures", "MA_Cancer_vs_PN.png"),
            os.path.join(self.base_dir, "figures", "Enrichment_Dotplots.png"),
            os.path.join(self.base_dir, "figures", "PPI_Network.png"),
            os.path.join(self.base_dir, "figures", "Clinical_Subgroups_Distribution.png"),
            os.path.join(self.base_dir, "figures", "Study_Workflow_Diagram.png"),
            # Tables
            os.path.join(self.base_dir, "results", "Enrichment", "GSEA_Results.csv"),
            os.path.join(self.base_dir, "results", "PPI", "PPI_Hub_Genes.csv"),
            os.path.join(self.base_dir, "results", "Clinical", "Cancer_Detailed_Clinical_Summary.csv")
        ]
        for fpath in required_files:
            self.assertTrue(os.path.exists(fpath), f"Required file missing: {fpath}")
            self.assertGreater(os.path.getsize(fpath), 0, f"File cannot be empty: {fpath}")

if __name__ == "__main__":
    unittest.main()
