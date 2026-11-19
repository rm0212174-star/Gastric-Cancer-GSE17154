import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = r"C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis"
enr_dir = os.path.join(BASE_DIR, "results", "Enrichment")
fig_dir = os.path.join(BASE_DIR, "figures")

files = [
    ("GO Biological Process (2021)", os.path.join(enr_dir, "GO_BP_Enrichment.csv"), "#337AB7"),
    ("KEGG Pathways (2021)", os.path.join(enr_dir, "KEGG_Enrichment.csv"), "#D9534F"),
    ("Reactome Pathways (2022)", os.path.join(enr_dir, "Reactome_Enrichment.csv"), "#5CB85C"),
    ("Ranked GSEA Coordinate Shifts", os.path.join(enr_dir, "GSEA_Results.csv"), "#8A6D3B")
]

fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=300)
axes = axes.flatten()

for idx, (title, csv_p, color) in enumerate(files):
    ax = axes[idx]
    if os.path.exists(csv_p):
        df = pd.read_csv(csv_p)
        if "Term" in df.columns:
            term_col = "Term"
            p_col = "P_Value" if "P_Value" in df.columns else "Adj_P_Value"
        elif "Pathway" in df.columns:
            term_col = "Pathway"
            p_col = "Adj_P_Value"
        else:
            term_col = df.columns[0]
            p_col = df.columns[1]
            
        top_df = df.sort_values(by=p_col).head(8).iloc[::-1]
        
        # Clean term names for readability
        clean_terms = [t.split(" (")[0][:45] for t in top_df[term_col]]
        p_vals = np.clip(top_df[p_col].astype(float).values, 1e-15, 1.0)
        neg_log_p = -np.log10(p_vals)
        
        bars = ax.barh(clean_terms, neg_log_p, color=color, alpha=0.85, edgecolor="black", height=0.6)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("-log10(P-value)" if "P_Value" in p_col else "-log10(Adj P-value)", fontsize=10)
        ax.grid(True, linestyle=":", alpha=0.5, axis="x")
        
plt.suptitle("Functional Enrichment & Ranked Pathway Analysis Overview\nGastric Cancer vs Paired Normal (GSE17154)", fontsize=14, fontweight="bold", y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

out1 = os.path.join(fig_dir, "Enrichment_Dotplots.png")
out2 = os.path.join(BASE_DIR, "Enrichment_Dotplots.png")
plt.savefig(out1)
plt.savefig(out2)
plt.close()
print(f"Generated {out1} and {out2}")
