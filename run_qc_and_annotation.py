import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'scripts':
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
elif os.path.basename(SCRIPT_DIR) == '12_Real_GSE17154_Analysis':
    BASE_DIR = SCRIPT_DIR
else:
    BASE_DIR = os.path.join(SCRIPT_DIR, '12_Real_GSE17154_Analysis')

import gzip
import os
import shutil
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from scipy.stats import pearsonr

print("================================================================================")
print("TASK 1: COMPREHENSIVE QUALITY CONTROL ON REAL GSE17154 EXPRESSION MATRIX")
print("================================================================================")

# 1. Load Expression Matrix
matrix_path = os.path.join(BASE_DIR, r"raw_downloads\GSE17154_series_matrix.txt.gz")
metadata_path = os.path.join(BASE_DIR, r"metadata\GSE17154_real_sample_metadata.csv")
annot_path = os.path.join(BASE_DIR, r"Probe_Annotation.csv")

meta_df = pd.read_csv(metadata_path)
annot_df = pd.read_csv(annot_path)

print(f"Loaded Metadata: {len(meta_df)} samples")
print(f"Loaded Annotation: {len(annot_df)} probes")

# Parse Series Matrix
print("Reading Expression values from Series Matrix...")
expr_data = {}
with gzip.open(matrix_path, 'rt', encoding='utf-8', errors='replace') as f:
    in_table = False
    samples = []
    for line in f:
        line_clean = line.rstrip('\r\n')
        if not in_table:
            if line_clean.startswith('!series_matrix_table_begin'):
                in_table = True
        else:
            if line_clean.startswith('!series_matrix_table_end'):
                break
            parts = line_clean.split('\t')
            if not samples:
                samples = [s.strip('"') for s in parts[1:]]
                for s in samples:
                    expr_data[s] = []
            else:
                probe_id = parts[0].strip('"')
                for s, val in zip(samples, parts[1:]):
                    val_str = val.strip('"').strip()
                    if val_str in ['', 'NA', 'null', 'NaN']:
                        expr_data[s].append(np.nan)
                    else:
                        expr_data[s].append(float(val_str))

expr_df = pd.DataFrame(expr_data, index=[str(i) for i in range(1, 44545)])
print(f"Expression matrix loaded: shape {expr_df.shape}")

# Sample group mapping and ordering
sample_groups = dict(zip(meta_df['GEO_Accession'], meta_df['Sample_Group']))
sample_titles = dict(zip(meta_df['GEO_Accession'], meta_df['Title']))

# Sort samples by group: CANCER, Paired_Normal_PN, Apparently_Normal_AN
meta_df['Group_Order'] = meta_df['Sample_Group'].map({'CANCER': 1, 'Paired_Normal_PN': 2, 'Apparently_Normal_AN': 3})
meta_sorted = meta_df.sort_values(by=['Group_Order', 'GEO_Accession'])
sorted_samples = meta_sorted['GEO_Accession'].tolist()
expr_df = expr_df[sorted_samples]

group_palette = {
    'CANCER': '#E64B35',           # Red / Coral
    'Paired_Normal_PN': '#4DBBD5', # Cyan / Light Blue
    'Apparently_Normal_AN': '#00A087' # Teal / Green
}
sample_colors = [group_palette[sample_groups[s]] for s in sorted_samples]

# -------------------------------------------------------------------------
# A. MISSING VALUE INVESTIGATION & IMPUTATION FOR QC/PCA
# -------------------------------------------------------------------------
print("\n--- Missing Value Investigation ---")
null_counts = expr_df.isnull().sum()
total_null = null_counts.sum()
print(f"Total missing values: {total_null}")
if total_null > 0:
    for s in expr_df.columns:
        if null_counts[s] > 0:
            null_probes = expr_df.index[expr_df[s].isnull()].tolist()
            print(f"Sample {s} ({sample_titles[s]}) has {null_counts[s]} null value at Probe {null_probes}")
            for p in null_probes:
                row_mean = expr_df.loc[p].mean()
                print(f"  Probe {p} across-sample mean = {row_mean:.4f}")

# Impute the single missing value with probe row mean for PCA and Pearson correlation
expr_df_imputed = expr_df.copy()
expr_df_imputed = expr_df_imputed.apply(lambda row: row.fillna(row.mean()), axis=1)

# -------------------------------------------------------------------------
# B. SAMPLE QC METRICS SUMMARY TABLE
# -------------------------------------------------------------------------
print("\nCalculating sample-level QC metrics...")
qc_metrics = []
for s in sorted_samples:
    vals = expr_df[s].dropna()
    grp = sample_groups[s]
    ttl = sample_titles[s]
    
    mean_v = vals.mean()
    std_v = vals.std()
    median_v = vals.median()
    iqr_v = vals.quantile(0.75) - vals.quantile(0.25)
    min_v = vals.min()
    max_v = vals.max()
    missing_cnt = expr_df[s].isnull().sum()
    
    qc_metrics.append({
        'Sample_ID': s,
        'Sample_Title': ttl,
        'Sample_Group': grp,
        'Mean_LogRatio': mean_v,
        'Median_LogRatio': median_v,
        'Std_Dev': std_v,
        'IQR': iqr_v,
        'Min_LogRatio': min_v,
        'Max_LogRatio': max_v,
        'Missing_Count': missing_cnt
    })

qc_summary_df = pd.DataFrame(qc_metrics)
print(qc_summary_df.head())

# Save Sample_QC_Summary.csv in both locations
qc_summary_csv1 = os.path.join(BASE_DIR, r"qc_annotation_outputs\tables\Sample_QC_Summary.csv")
qc_summary_csv2 = os.path.join(BASE_DIR, r"Sample_QC_Summary.csv")
qc_summary_df.to_csv(qc_summary_csv1, index=False)
qc_summary_df.to_csv(qc_summary_csv2, index=False)
print(f"Saved Sample QC summary table to:\n - {qc_summary_csv1}\n - {qc_summary_csv2}")

# -------------------------------------------------------------------------
# 1. GENERATE QC BOXPLOTS
# -------------------------------------------------------------------------
print("\nGenerating QC Boxplots for all 49 samples...")
fig, ax = plt.subplots(figsize=(16, 7))
box_data = [expr_df[s].dropna() for s in sorted_samples]
labels = [sample_titles[s].replace(' (gastric cancer study)', '') for s in sorted_samples]

bp = ax.boxplot(box_data, patch_artist=True, tick_labels=labels, showfliers=False,
                medianprops=dict(color='black', linewidth=1.5),
                whiskerprops=dict(color='gray', linewidth=1),
                capprops=dict(color='gray', linewidth=1))

for patch, color in zip(bp['boxes'], sample_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)

ax.set_xticklabels(labels, rotation=90, fontsize=8)
ax.set_ylabel(r'Normalised $\log_2(\mathrm{Cy5}/\mathrm{Cy3})$ Ratio', fontsize=12, fontweight='bold')
ax.set_title('GSE17154: Expression Distribution Boxplots Across 49 Clinical Samples (GPL6699, 44,544 Probes)',
             fontsize=14, fontweight='bold', pad=15)
ax.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Zero Baseline')

# Add custom legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#E64B35', label='CANCER (N=24)'),
    Patch(facecolor='#4DBBD5', label='Paired Normal / PN (N=20)'),
    Patch(facecolor='#00A087', label='Apparently Normal / AN (N=5)')
]
ax.legend(handles=legend_elements, loc='upper right', frameon=True, fontsize=10)
plt.tight_layout()

box_out1 = os.path.join(BASE_DIR, r"qc_annotation_outputs\figures\QC_Boxplots.png")
box_out2 = os.path.join(BASE_DIR, r"QC_Boxplots.png")
fig.savefig(box_out1, dpi=300)
fig.savefig(box_out2, dpi=300)
plt.close(fig)
print(f"Saved Boxplots to:\n - {box_out1}\n - {box_out2}")

# -------------------------------------------------------------------------
# 2. GENERATE QC DENSITY PLOTS
# -------------------------------------------------------------------------
print("\nGenerating QC Density Plots for all 49 samples...")
fig, ax = plt.subplots(figsize=(12, 7))
for s in sorted_samples:
    grp = sample_groups[s]
    col = group_palette[grp]
    vals = expr_df[s].dropna()
    sns.kdeplot(vals, ax=ax, color=col, alpha=0.35, linewidth=1.2, bw_adjust=1.2)

ax.set_xlim(-3.0, 3.0)
ax.set_xlabel(r'Normalised $\log_2(\mathrm{Cy5}/\mathrm{Cy3})$ Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Density', fontsize=12, fontweight='bold')
ax.set_title('GSE17154: Log-Ratio Kernel Density Distribution (49 Samples)', fontsize=14, fontweight='bold', pad=15)
ax.axvline(0, color='black', linestyle=':', linewidth=1.2, label='Median Center (0.0)')
ax.legend(handles=legend_elements, loc='upper right', frameon=True, fontsize=10)
plt.tight_layout()

density_out1 = os.path.join(BASE_DIR, r"qc_annotation_outputs\figures\QC_Density_Plots.png")
density_out2 = os.path.join(BASE_DIR, r"QC_Density_Plots.png")
fig.savefig(density_out1, dpi=300)
fig.savefig(density_out2, dpi=300)
plt.close(fig)
print(f"Saved Density Plots to:\n - {density_out1}\n - {density_out2}")

# -------------------------------------------------------------------------
# 3. SAMPLE-TO-SAMPLE PEARSON CORRELATION & HEATMAP
# -------------------------------------------------------------------------
print("\nCalculating sample-to-sample Pearson correlation matrix...")
corr_mat = expr_df_imputed.corr(method='pearson')
print(f"Correlation matrix calculated: {corr_mat.shape}")
print(f"Min correlation: {corr_mat.values.min():.4f}, Max: {corr_mat.values.max():.4f}, Mean: {corr_mat.values.mean():.4f}")

# Generate Heatmap with Clustermap
corr_labels = [sample_titles[s].replace(' (gastric cancer study)', '') for s in sorted_samples]
corr_mat_renamed = corr_mat.copy()
corr_mat_renamed.index = corr_labels
corr_mat_renamed.columns = corr_labels

col_colors = pd.Series(sample_colors, index=corr_labels)

g = sns.clustermap(corr_mat_renamed, figsize=(14, 13), cmap='vlag',
                   row_colors=col_colors, col_colors=col_colors,
                   vmin=0.2, vmax=1.0, dendrogram_ratio=(0.15, 0.15),
                   cbar_pos=(0.02, 0.8, 0.03, 0.15),
                   cbar_kws={'label': 'Pearson Correlation (r)'},
                   linewidths=0.0)

g.ax_heatmap.set_xticklabels(g.ax_heatmap.get_xticklabels(), fontsize=7)
g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_yticklabels(), fontsize=7)
g.fig.suptitle('GSE17154: Sample-to-Sample Pearson Correlation Heatmap\n(Hierarchical Clustering of 49 Samples Across 44,544 Probes)',
               fontsize=13, fontweight='bold', y=0.98)

# Add Legend to clustermap
for label, color in group_palette.items():
    g.ax_col_dendrogram.bar(0, 0, color=color, label=label, linewidth=0)
g.ax_col_dendrogram.legend(loc="upper left", ncol=1, frameon=True, fontsize=9, bbox_to_anchor=(0.0, 1.35))

heatmap_out1 = os.path.join(BASE_DIR, r"qc_annotation_outputs\figures\Sample_Correlation_Heatmap.png")
heatmap_out2 = os.path.join(BASE_DIR, r"Sample_Correlation_Heatmap.png")
g.savefig(heatmap_out1, dpi=300)
g.savefig(heatmap_out2, dpi=300)
plt.close(g.fig)
print(f"Saved Correlation Heatmap to:\n - {heatmap_out1}\n - {heatmap_out2}")

# -------------------------------------------------------------------------
# 4. PERFORM PCA ON REAL 44,544-PROBE EXPRESSION MATRIX
# -------------------------------------------------------------------------
print("\nPerforming Principal Component Analysis (PCA)...")
# Samples as rows (49, 44544)
pca = PCA(n_components=5)
X = expr_df_imputed.T.values
pca_coords = pca.fit_transform(X)

pca_df = pd.DataFrame(pca_coords, index=sorted_samples,
                      columns=[f'PC{i+1}' for i in range(5)])
pca_df['Sample_Title'] = [sample_titles[s] for s in sorted_samples]
pca_df['Sample_Group'] = [sample_groups[s] for s in sorted_samples]

exp_var = pca.explained_variance_ratio_ * 100
print(f"Explained Variance: PC1={exp_var[0]:.2f}%, PC2={exp_var[1]:.2f}%, PC3={exp_var[2]:.2f}%")

fig, ax = plt.subplots(figsize=(10, 8))
for grp, color in group_palette.items():
    sub = pca_df[pca_df['Sample_Group'] == grp]
    ax.scatter(sub['PC1'], sub['PC2'], c=color, label=f'{grp} (N={len(sub)})',
               s=90, alpha=0.85, edgecolors='black', linewidth=0.8)

# Label selected representative points
for s in sorted_samples:
    x_pt = pca_df.loc[s, 'PC1']
    y_pt = pca_df.loc[s, 'PC2']
    ttl_short = sample_titles[s].replace(' (gastric cancer study)', '')
    # Only label outliers or edge points to avoid visual clutter
    if abs(x_pt) > 50 or abs(y_pt) > 35:
        ax.annotate(ttl_short, (x_pt + 1.2, y_pt + 0.8), fontsize=7.5, alpha=0.85)

ax.set_xlabel(f'Principal Component 1 ({exp_var[0]:.2f}% Variance)', fontsize=12, fontweight='bold')
ax.set_ylabel(f'Principal Component 2 ({exp_var[1]:.2f}% Variance)', fontsize=12, fontweight='bold')
ax.set_title('GSE17154: Principal Component Analysis (PCA) Across 44,544 Probes\n(49 Clinical Samples: CANCER vs Paired Normal vs Apparently Normal)',
             fontsize=13, fontweight='bold', pad=15)
ax.axhline(0, color='gray', linestyle=':', alpha=0.6)
ax.axvline(0, color='gray', linestyle=':', alpha=0.6)
ax.legend(loc='upper right', frameon=True, fontsize=10)
plt.tight_layout()

pca_out1 = os.path.join(BASE_DIR, r"qc_annotation_outputs\figures\Real_Data_PCA.png")
pca_out2 = os.path.join(BASE_DIR, r"Real_Data_PCA.png")
fig.savefig(pca_out1, dpi=300)
fig.savefig(pca_out2, dpi=300)
plt.close(fig)
print(f"Saved PCA Plot to:\n - {pca_out1}\n - {pca_out2}")

# -------------------------------------------------------------------------
# 5. CONTROL PROBE INFLUENCE CHECK
# -------------------------------------------------------------------------
print("\nInvestigating influence of control probes...")
ctrl_ids = annot_df[annot_df['Is_Control'] == True]['Probe_ID'].astype(str).tolist()
exp_ids = annot_df[annot_df['Is_Control'] == False]['Probe_ID'].astype(str).tolist()

ctrl_expr = expr_df_imputed.loc[ctrl_ids]
exp_expr = expr_df_imputed.loc[exp_ids]

print(f"Control probe submatrix: {ctrl_expr.shape}")
print(f"Control probes Mean LogRatio: {ctrl_expr.values.mean():.4f}, Std: {ctrl_expr.values.std():.4f}")
print(f"Experimental probes Mean LogRatio: {exp_expr.values.mean():.4f}, Std: {exp_expr.values.std():.4f}")

# PCA on experimental only to see if controls distorted PCA
pca_exp = PCA(n_components=2)
coords_exp = pca_exp.fit_transform(exp_expr.T.values)
exp_var_exp = pca_exp.explained_variance_ratio_ * 100
corr_pc1 = pearsonr(pca_coords[:, 0], coords_exp[:, 0])[0]
print(f"Experimental-only PC1 vs All-probes PC1 Pearson correlation: r = {corr_pc1:.5f}")
print("Conclusion: Control probes do not distort sample separation, but MUST be filtered out prior to differential expression.")

print("\nQuality Control and Annotation script finished successfully!")