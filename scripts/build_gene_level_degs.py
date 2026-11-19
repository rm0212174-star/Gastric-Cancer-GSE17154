import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'scripts':
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
elif os.path.basename(SCRIPT_DIR) == '12_Real_GSE17154_Analysis':
    BASE_DIR = SCRIPT_DIR
else:
    BASE_DIR = os.path.join(SCRIPT_DIR, '12_Real_GSE17154_Analysis')

base_dir = BASE_DIR

for c in ['Cancer_vs_PN', 'Cancer_vs_AN', 'PN_vs_AN']:
    full_path = os.path.join(base_dir, "results", "DEG", f"DEG_{c}_Full.csv")
    df = pd.read_csv(full_path)
    
    # Filter out Unmapped or non-standard identifiers
    df_valid = df[df['Gene_Symbol'] != 'Unmapped'].copy()
    
    # Gene-level summarization: probe with maximum absolute moderated t-statistic
    df_valid['abs_t'] = df_valid['Moderated_t'].abs()
    idx_max = df_valid.groupby('Gene_Symbol')['abs_t'].idxmax()
    gene_df = df_valid.loc[idx_max].sort_values(by='Adj_P_Value').reset_index(drop=True)
    gene_df = gene_df.drop(columns=['abs_t'])
    
    # Save gene-level full table
    gene_full_out = os.path.join(base_dir, "results", "DEG", f"DEG_{c}_Gene_Level_Full.csv")
    gene_df.to_csv(gene_full_out, index=False)
    
    # Save gene-level strict DEGs (|Log2FC| >= 1.0 & FDR < 0.05)
    gene_strict = gene_df[(gene_df['Adj_P_Value'] < 0.05) & (gene_df['Log2FC'].abs() >= 1.0)]
    gene_strict_out = os.path.join(base_dir, "results", "DEG", f"DEG_{c}_Gene_Level_Strict_FDR05_FC2.csv")
    gene_strict.to_csv(gene_strict_out, index=False)
    
    up = gene_strict[gene_strict['Log2FC'] >= 1.0]
    down = gene_strict[gene_strict['Log2FC'] <= -1.0]
    
    print(f"=== {c} GENE-LEVEL SUMMARY ===")
    print(f"Total Unique Genes Analyzed: {len(gene_df):,}")
    print(f"Significant Genes (FDR < 0.05): {len(gene_df[gene_df['Adj_P_Value'] < 0.05]):,}")
    print(f"Strict Significant Genes (|Log2FC| >= 1.0 & FDR < 0.05): {len(gene_strict):,} (Up: {len(up):,}, Down: {len(down):,})")

print("\nGene-level summarization tables saved successfully!")
