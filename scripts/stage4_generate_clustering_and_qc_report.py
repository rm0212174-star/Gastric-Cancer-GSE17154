import os
import gzip
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform

BASE_DIR = r"C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis"
matrix_path = os.path.join(BASE_DIR, "raw_downloads", "GSE17154_series_matrix.txt.gz")
meta_path = os.path.join(BASE_DIR, "FINAL_SAMPLE_METADATA.csv")

print("Reading Expression values from GSE17154_series_matrix.txt.gz...")
in_table = False
table_lines = []
with gzip.open(matrix_path, 'rt', encoding='utf-8') as f:
    for line in f:
        line_clean = line.strip()
        if line_clean.startswith('!series_matrix_table_begin'):
            in_table = True
            continue
        if line_clean.startswith('!series_matrix_table_end'):
            break
        if in_table:
            table_lines.append(line)

expr_df = pd.read_csv(io.StringIO("".join(table_lines)), sep='\t', index_col=0)
expr_df.columns = [c.strip('"') for c in expr_df.columns]
expr_df.index = expr_df.index.astype(str)

print(f"Expression matrix loaded: shape {expr_df.shape}")

# Save the processed expression matrix to data/processed_matrix
os.makedirs(os.path.join(BASE_DIR, "data", "processed_matrix"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data", "processed"), exist_ok=True)
csv_out1 = os.path.join(BASE_DIR, "data", "processed_matrix", "GSE17154_Expression_Matrix.csv")
csv_out2 = os.path.join(BASE_DIR, "data", "processed", "GSE17154_Expression_Matrix.csv")
expr_df.to_csv(csv_out1)
expr_df.to_csv(csv_out2)
print(f"Saved Expression Matrix CSV to {csv_out1}")

meta_df = pd.read_csv(meta_path)

# Fill 1 missing value with probe mean
expr_filled = expr_df.apply(lambda row: row.fillna(row.mean()), axis=1)

# Sample-to-sample correlation
corr_mat = expr_filled.corr(method="pearson")
dist_mat = 1.0 - corr_mat

# Hierarchical clustering
linkage_mat = sch.linkage(squareform(dist_mat), method="average")

# Map group colors
color_map = {
    "CANCER": "#D9534F",
    "Paired_Normal_PN": "#337AB7",
    "Apparently_Normal_AN": "#5CB85C"
}
meta_dict = meta_df.set_index("Sample_ID")["Statistical_Group"].to_dict()

plt.figure(figsize=(15, 8), dpi=300)
dendro = sch.dendrogram(
    linkage_mat,
    labels=expr_df.columns,
    leaf_rotation=90,
    leaf_font_size=9,
    above_threshold_color="#555555"
)

# Color the labels
ax = plt.gca()
xlbls = ax.get_xmajorticklabels()
for lbl in xlbls:
    s_id = lbl.get_text()
    grp = meta_dict.get(s_id, "CANCER")
    lbl.set_color(color_map.get(grp, "#000000"))

plt.title("Sample Hierarchical Clustering Dendrogram (Average Linkage, 1 - Pearson Correlation Distance)\nGEO GSE17154 (49 Samples, 44,544 Probes)", fontsize=13, fontweight="bold", pad=12)
plt.ylabel("Distance (1 - Pearson r)", fontsize=11)
plt.xlabel("Sample Accession (Red = CANCER, Blue = Paired Normal, Green = Apparently Normal)", fontsize=11)

# Custom legend
custom_lines = [
    plt.Line2D([0], [0], color="#D9534F", lw=3, label="Gastric Cancer (N=24)"),
    plt.Line2D([0], [0], color="#337AB7", lw=3, label="Paired Normal (PN, N=20)"),
    plt.Line2D([0], [0], color="#5CB85C", lw=3, label="Apparently Normal (AN, N=5)")
]
plt.legend(handles=custom_lines, loc="upper right", frameon=True, fontsize=10)

plt.tight_layout()
fig_out1 = os.path.join(BASE_DIR, "figures", "Sample_Clustering.png")
fig_out2 = os.path.join(BASE_DIR, "Sample_Clustering.png")
plt.savefig(fig_out1)
plt.savefig(fig_out2)
plt.close()

print(f"Generated {fig_out1} and {fig_out2} successfully!")
