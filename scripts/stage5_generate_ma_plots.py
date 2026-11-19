import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = r"C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis"
deg_dir = os.path.join(BASE_DIR, "results", "DEG")
fig_dir = os.path.join(BASE_DIR, "figures")
expr_path = os.path.join(BASE_DIR, "data", "processed_matrix", "GSE17154_Expression_Matrix.csv")

expr_df = pd.read_csv(expr_path, index_col=0)
expr_mean = expr_df.mean(axis=1)
expr_mean.index = expr_mean.index.astype(str)

contrasts = ["Cancer_vs_PN", "Cancer_vs_AN", "PN_vs_AN"]

for c_name in contrasts:
    csv_path = os.path.join(deg_dir, f"DEG_{c_name}_Full.csv")
    df = pd.read_csv(csv_path)
    df["Probe_ID"] = df["Probe_ID"].astype(str)
    
    # Map average expression (A in MA plot)
    df["Average_Expression"] = df["Probe_ID"].map(expr_mean)
    
    # Identify significant probes (|Log2FC| >= 1.0 and Adj_P_Value < 0.05)
    df["Strict_DEG"] = (df["Adj_P_Value"] < 0.05) & (df["Log2FC"].abs() >= 1.0)
    df["Significant"] = df["Adj_P_Value"] < 0.05
    
    plt.figure(figsize=(9, 6), dpi=300)
    
    # Plot non-significant probes in grey
    non_sig = df[~df["Significant"]]
    plt.scatter(non_sig["Average_Expression"], non_sig["Log2FC"], c="#B0B0B0", s=6, alpha=0.3, label="Not Significant")
    
    # Plot significant probes (|Log2FC| < 1 but Adj_P_Value < 0.05) in yellow/orange
    fdr_only = df[df["Significant"] & ~df["Strict_DEG"]]
    if len(fdr_only) > 0:
        plt.scatter(fdr_only["Average_Expression"], fdr_only["Log2FC"], c="#F0AD4E", s=10, alpha=0.5, label=f"FDR < 0.05 (|Log2FC| < 1, N={len(fdr_only)})")
        
    # Plot strict upregulated in red
    up = df[df["Strict_DEG"] & (df["Log2FC"] >= 1.0)]
    if len(up) > 0:
        plt.scatter(up["Average_Expression"], up["Log2FC"], c="#D9534F", s=14, alpha=0.8, label=f"Strict Up (Log2FC >= 1, N={len(up)})")
        
    # Plot strict downregulated in blue
    down = df[df["Strict_DEG"] & (df["Log2FC"] <= -1.0)]
    if len(down) > 0:
        plt.scatter(down["Average_Expression"], down["Log2FC"], c="#337AB7", s=14, alpha=0.8, label=f"Strict Down (Log2FC <= -1, N={len(down)})")
        
    plt.axhline(0, color="black", linestyle="--", linewidth=1.0)
    plt.axhline(1.0, color="grey", linestyle=":", linewidth=0.8)
    plt.axhline(-1.0, color="grey", linestyle=":", linewidth=0.8)
    
    plt.title(f"MA Plot: {c_name.replace('_', ' ')} (limma Empirical Bayes)\nGSE17154 Microarray (40,197 Experimental Probes)", fontsize=11, fontweight="bold", pad=10)
    plt.xlabel("Average Expression (A = Mean Normalized Log2 Ratio)", fontsize=10)
    plt.ylabel("Fold Change (M = Contrast Log2 Fold Change)", fontsize=10)
    plt.legend(loc="upper right", frameon=True, fontsize=9)
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    
    out1 = os.path.join(fig_dir, f"MA_{c_name}.png")
    out2 = os.path.join(BASE_DIR, f"MA_{c_name}.png")
    plt.savefig(out1)
    plt.savefig(out2)
    plt.close()
    print(f"Generated {out1} and {out2}")
