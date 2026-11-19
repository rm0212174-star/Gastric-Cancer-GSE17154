import pandas as pd
import numpy as np

for c in ['Cancer_vs_PN', 'Cancer_vs_AN', 'PN_vs_AN']:
    df = pd.read_csv(fr'12_Real_GSE17154_Analysis\results\DEG\DEG_{c}_Full.csv')
    sig_any = df[df['Adj_P_Value'] < 0.05]
    strict = df[(df['Adj_P_Value'] < 0.05) & (df['Log2FC'].abs() >= 1.0)]
    up = df[(df['Adj_P_Value'] < 0.05) & (df['Log2FC'] >= 1.0)]
    down = df[(df['Adj_P_Value'] < 0.05) & (df['Log2FC'] <= -1.0)]
    
    unique_genes_strict = strict['Gene_Symbol'].dropna().unique()
    unique_genes_strict = [g for g in unique_genes_strict if g != 'Unmapped' and not g.startswith('suid=')]
    
    unique_genes_up = up['Gene_Symbol'].dropna().unique()
    unique_genes_up = [g for g in unique_genes_up if g != 'Unmapped' and not g.startswith('suid=')]
    
    unique_genes_down = down['Gene_Symbol'].dropna().unique()
    unique_genes_down = [g for g in unique_genes_down if g != 'Unmapped' and not g.startswith('suid=')]
    
    print(f"=== {c} ===")
    print(f"Total Probes: {len(df):,}")
    print(f"Significant Probes (FDR < 0.05): {len(sig_any):,}")
    print(f"Strict Significant Probes (|Log2FC| >= 1.0 & FDR < 0.05): {len(strict):,} (Up: {len(up):,}, Down: {len(down):,})")
    print(f"Unique Strict Gene Symbols: {len(unique_genes_strict):,} (Up: {len(unique_genes_up):,}, Down: {len(unique_genes_down):,})")
    print(f"Min FDR: {df['Adj_P_Value'].min():.4e}")
