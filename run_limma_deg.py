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
import pandas as pd
import numpy as np
import scipy.stats as stats
import scipy.special as special
from statsmodels.stats.multitest import multipletests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

print("================================================================================")
print("DIFFERENTIAL EXPRESSION ANALYSIS: LIMMA EMPIRICAL BAYES MODELING")
print("================================================================================")

# Paths
matrix_path = os.path.join(BASE_DIR, r"raw_downloads\GSE17154_series_matrix.txt.gz")
metadata_path = os.path.join(BASE_DIR, r"metadata\GSE17154_real_sample_metadata.csv")
annot_path = os.path.join(BASE_DIR, r"Probe_Annotation.csv")

meta_df = pd.read_csv(metadata_path)
annot_df = pd.read_csv(annot_path)

# Verify 49 samples and 3 groups
print(f"Total samples in metadata: {len(meta_df)}")
print(meta_df['Sample_Group'].value_counts())

# Load Expression matrix
print("\nLoading expression values...")
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
                for s, val in zip(samples, parts[1:]):
                    val_str = val.strip('"').strip()
                    if val_str in ['', 'NA', 'null', 'NaN']:
                        expr_data[s].append(np.nan)
                    else:
                        expr_data[s].append(float(val_str))

probe_ids = [str(i) for i in range(1, 44545)]
expr_df = pd.DataFrame(expr_data, index=probe_ids)
print(f"Full Expression Matrix shape: {expr_df.shape}")

# Sample grouping
sample_order = meta_df['GEO_Accession'].tolist()
expr_df = expr_df[sample_order]
groups = meta_df['Sample_Group'].values

# Filter out control probes
annot_df['Probe_ID_str'] = annot_df['Probe_ID'].astype(str)
annot_dict = annot_df.set_index('Probe_ID_str').to_dict('index')

exp_probe_ids = annot_df[annot_df['Is_Control'] == False]['Probe_ID_str'].tolist()
print(f"Total Experimental Probes for analysis: {len(exp_probe_ids):,} (filtering {len(annot_df) - len(exp_probe_ids):,} controls)")

expr_exp = expr_df.loc[exp_probe_ids].copy()

# Handle single missing value: probe 24 in GSM429144 (CANCER - 9)
# Impute using probe row mean across cancer samples
null_probes = expr_exp.index[expr_exp.isnull().any(axis=1)].tolist()
print(f"Probes with missing values in experimental set: {null_probes}")
for p in null_probes:
    row_mean = expr_exp.loc[p].mean()
    expr_exp.loc[p] = expr_exp.loc[p].fillna(row_mean)

# -------------------------------------------------------------------------
# LIMMA EMPIRICAL BAYES IMPLEMENTATION
# -------------------------------------------------------------------------
def fit_limma_ebayes(Y, design, contrasts):
    """
    Fits linear models and empirical Bayes moderation matching limma::lmFit & eBayes.
    Y: (n_probes, n_samples)
    design: (n_samples, n_coef)
    contrasts: (n_coef, n_contrasts)
    """
    n_probes, n_samples = Y.shape
    p = design.shape[1]
    df_residual = n_samples - p
    
    # OLS fit: beta = (X'X)^-1 X' Y'
    XtX = design.T @ design
    XtX_inv = np.linalg.pinv(XtX)
    beta = XtX_inv @ design.T @ Y.T # shape: (p, n_probes)
    
    # Residuals & residual variance (s2)
    fitted = design @ beta # (n_samples, n_probes)
    residuals = Y.T - fitted
    sigma2 = np.sum(residuals**2, axis=0) / df_residual # (n_probes,)
    
    # Contrast coefficients: beta_c = C' beta
    beta_c = contrasts.T @ beta # (n_contrasts, n_probes)
    
    # Contrast covariance scaling: v_c = diag(C' (X'X)^-1 C)
    C_cov = contrasts.T @ XtX_inv @ contrasts # (n_contrasts, n_contrasts)
    v_c = np.diag(C_cov)[:, np.newaxis] # (n_contrasts, 1)
    
    # Standard empirical Bayes squeeze of sigma2 towards s02 with d0 degrees of freedom
    # Smyth 2004: Linear Models and Empirical Bayes Methods for Assessing Differential Expression
    log_s2 = np.log(np.maximum(sigma2, 1e-12))
    d = df_residual
    
    # Method of moments for d0 and s02 based on trigamma
    e = log_s2 - special.digamma(d / 2.0) + np.log(d / 2.0)
    e_mean = np.mean(e)
    e_var = np.var(e, ddof=1)
    trigamma_d = special.polygamma(1, d / 2.0)
    
    if e_var > trigamma_d:
        # Solve for d0 numerically
        from scipy.optimize import root_scalar
        def obj(x):
            return special.polygamma(1, x / 2.0) - (e_var - trigamma_d)
        res = root_scalar(obj, bracket=[0.01, 1000.0], method='brentq')
        d0 = res.root
    else:
        d0 = 10.0 # Robust default prior df
        
    s02 = np.exp(e_mean + special.digamma(d0 / 2.0) - np.log(d0 / 2.0))
    
    # Moderated variance: s2_post = (d0 * s02 + d * s2) / (d0 + d)
    df_total = d0 + df_residual
    s2_post = (d0 * s02 + d * sigma2) / df_total
    s_post = np.sqrt(s2_post)
    
    # Moderated t-statistics for each contrast: t = beta_c / (s_post * sqrt(v_c))
    se_c = np.sqrt(v_c) * s_post[np.newaxis, :] # (n_contrasts, n_probes)
    t_stat = beta_c / se_c
    
    # Two-sided p-values from Student t distribution with df_total
    p_val = 2.0 * (1.0 - stats.t.cdf(np.abs(t_stat), df=df_total))
    
    return beta_c, t_stat, p_val, df_total, d0, s02

# Design matrix: ~ 0 + Group (levels: CANCER, Paired_Normal_PN, Apparently_Normal_AN)
group_levels = ['CANCER', 'Paired_Normal_PN', 'Apparently_Normal_AN']
design = np.zeros((len(groups), len(group_levels)))
for i, g in enumerate(groups):
    col = group_levels.index(g)
    design[i, col] = 1.0

print(f"Design Matrix constructed: {design.shape}")
print(f"Group sample counts: CANCER={int(design[:, 0].sum())}, PN={int(design[:, 1].sum())}, AN={int(design[:, 2].sum())}")

# Contrasts:
# 1. Cancer vs PN: CANCER - PN = [1, -1, 0]
# 2. Cancer vs AN: CANCER - AN = [1, 0, -1]
# 3. PN vs AN: PN - AN = [0, 1, -1]
contrast_names = ['Cancer_vs_PN', 'Cancer_vs_AN', 'PN_vs_AN']
contrasts = np.array([
    [1.0,  1.0,  0.0],  # CANCER
    [-1.0,  0.0,  1.0],  # Paired_Normal_PN
    [0.0, -1.0, -1.0]   # Apparently_Normal_AN
])

print("\nFitting Empirical Bayes Moderated Linear Models across 40,197 probes...")
Y = expr_exp.values # (40197, 49)
beta_c, t_stat, p_val, df_total, d0, s02 = fit_limma_ebayes(Y, design, contrasts)

print(f"Empirical Bayes Prior: d0 = {d0:.2f}, s02 = {s02:.4f}, Total df = {df_total:.2f}")

# -------------------------------------------------------------------------
# COMPILE RESULTS PER CONTRAST & FDR CORRECTION
# -------------------------------------------------------------------------
contrast_results = {}

for c_idx, c_name in enumerate(contrast_names):
    lfc = beta_c[c_idx]
    t = t_stat[c_idx]
    p = p_val[c_idx]
    
    # Benjamini-Hochberg FDR
    reject, padj, _, _ = multipletests(p, method='fdr_bh')
    
    res_df = pd.DataFrame({
        'Probe_ID': exp_probe_ids,
        'Gene_Symbol': [annot_dict[pid]['Gene_Symbol'] for pid in exp_probe_ids],
        'Gene_Description': [annot_dict[pid]['Gene_Description'] for pid in exp_probe_ids],
        'Log2FC': lfc,
        'Moderated_t': t,
        'P_Value': p,
        'Adj_P_Value': padj
    })
    
    # Sort by significance (P_Value)
    res_df = res_df.sort_values(by='P_Value').reset_index(drop=True)
    contrast_results[c_name] = res_df
    
    # Summary of DEGs: padj < 0.05 and |log2FC| >= 1.0 (2-fold)
    sig_genes_fdr05 = res_df[res_df['Adj_P_Value'] < 0.05]
    sig_genes_fc2 = res_df[(res_df['Adj_P_Value'] < 0.05) & (res_df['Log2FC'].abs() >= 1.0)]
    up_fc2 = res_df[(res_df['Adj_P_Value'] < 0.05) & (res_df['Log2FC'] >= 1.0)]
    down_fc2 = res_df[(res_df['Adj_P_Value'] < 0.05) & (res_df['Log2FC'] <= -1.0)]
    
    print(f"\n--- Contrast: {c_name} ---")
    print(f"Total probes tested: {len(res_df):,}")
    print(f"FDR < 0.05 (any FC): {len(sig_genes_fdr05):,}")
    print(f"FDR < 0.05 & |Log2FC| >= 1.0: {len(sig_genes_fc2):,} (Up: {len(up_fc2):,}, Down: {len(down_fc2):,})")
    print("Top 5 differentially expressed probes:")
    print(res_df[['Probe_ID', 'Gene_Symbol', 'Log2FC', 'Moderated_t', 'P_Value', 'Adj_P_Value']].head())
    
    # Save full table and top DEG table
    full_table_path = os.path.join(BASE_DIR, f"deg_outputs/tables\DEG_{c_name}_Full.csv")
    top_table_path = os.path.join(BASE_DIR, f"deg_outputs/tables\DEG_{c_name}_Top_FDR05_FC2.csv")
    res_df.to_csv(full_table_path, index=False)
    res_df.to_csv(os.path.join(BASE_DIR, "results", "DEG", f"DEG_{c_name}_Full.csv"), index=False)
    sig_genes_fc2.to_csv(top_table_path, index=False)
    sig_genes_fc2.to_csv(os.path.join(BASE_DIR, "results", "DEG", f"DEG_{c_name}_Top_FDR05_FC2.csv"), index=False)

# -------------------------------------------------------------------------
# GENERATE VOLCANO PLOTS FOR EACH CONTRAST
# -------------------------------------------------------------------------
print("\nGenerating Volcano plots...")
for c_name in contrast_names:
    df = contrast_results[c_name]
    
    fig, ax = plt.subplots(figsize=(9, 7))
    logp = -np.log10(np.maximum(df['P_Value'], 1e-300))
    
    # Classify points
    is_up = (df['Adj_P_Value'] < 0.05) & (df['Log2FC'] >= 1.0)
    is_down = (df['Adj_P_Value'] < 0.05) & (df['Log2FC'] <= -1.0)
    is_ns = ~(is_up | is_down)
    
    ax.scatter(df.loc[is_ns, 'Log2FC'], logp[is_ns], c='#B0BEC5', alpha=0.35, s=12, label='Not Significant')
    ax.scatter(df.loc[is_up, 'Log2FC'], logp[is_up], c='#E53935', alpha=0.75, s=18, label=f'Up-regulated (N={is_up.sum():,})')
    ax.scatter(df.loc[is_down, 'Log2FC'], logp[is_down], c='#1E88E5', alpha=0.75, s=18, label=f'Down-regulated (N={is_down.sum():,})')
    
    # Cutoff lines
    ax.axvline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(-1.0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    
    # FDR 0.05 p-value threshold line
    if len(df[df['Adj_P_Value'] < 0.05]) > 0:
        max_p_fdr05 = df[df['Adj_P_Value'] < 0.05]['P_Value'].max()
        thresh_logp = -np.log10(max_p_fdr05)
        ax.axhline(thresh_logp, color='darkred', linestyle=':', linewidth=1.2, label=f'FDR < 0.05 (p={max_p_fdr05:.2e})')
    
    # Label top 10 genes
    top_label_df = df[(is_up | is_down)].head(10)
    for idx, r in top_label_df.iterrows():
        y_val = -np.log10(max(r['P_Value'], 1e-300))
        ax.annotate(r['Gene_Symbol'], (r['Log2FC'], y_val),
                    fontsize=8, fontweight='bold', alpha=0.9,
                    xytext=(4, 4), textcoords='offset points')
                    
    ax.set_xlabel(r'$\log_2$ Fold Change', fontsize=12, fontweight='bold')
    ax.set_ylabel(r'$-\log_{10}(\mathrm{p\text{-}value})$', fontsize=12, fontweight='bold')
    ax.set_title(f'Volcano Plot: {c_name.replace("_", " ")}\n(Empirical Bayes Moderated Linear Model, 40,197 Probes)',
                 fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='upper right', frameon=True, fontsize=9)
    plt.tight_layout()
    
    volcano_out1 = os.path.join(BASE_DIR, f"deg_outputs/figures\Volcano_{c_name}.png")
    volcano_out2 = os.path.join(BASE_DIR, f"Volcano_{c_name}.png")
    fig.savefig(volcano_out1, dpi=300)
    fig.savefig(volcano_out2, dpi=300)
    plt.close(fig)
    print(f"Saved Volcano plot: {volcano_out1}")

# -------------------------------------------------------------------------
# GENERATE HEATMAPS FOR TOP 50 DEGS PER CONTRAST
# -------------------------------------------------------------------------
print("\nGenerating Heatmaps for top differentially expressed genes...")
# Prepare sample group annotations for heatmap columns
group_colors = {
    'CANCER': '#E64B35',
    'Paired_Normal_PN': '#4DBBD5',
    'Apparently_Normal_AN': '#00A087'
}
col_colors = pd.Series([group_colors[g] for g in groups], index=sample_order)

for c_name in contrast_names:
    df = contrast_results[c_name]
    top50 = df.head(50)
    top_pids = top50['Probe_ID'].tolist()
    
    sub_expr = expr_exp.loc[top_pids, sample_order]
    # Z-score row normalization across samples
    sub_z = sub_expr.apply(lambda r: (r - r.mean()) / (r.std() if r.std() > 0 else 1.0), axis=1)
    
    # Row labels: Gene_Symbol (Probe_ID)
    row_labels = [f"{annot_dict[pid]['Gene_Symbol']} ({pid})" for pid in top_pids]
    sub_z.index = row_labels
    
    g = sns.clustermap(sub_z, figsize=(14, 13), cmap='vlag',
                       col_colors=col_colors, col_cluster=True, row_cluster=True,
                       vmin=-2.5, vmax=2.5, dendrogram_ratio=(0.15, 0.15),
                       cbar_pos=(0.02, 0.8, 0.03, 0.15),
                       cbar_kws={'label': 'Z-score of Log-Ratio'},
                       linewidths=0.0)
                       
    g.ax_heatmap.set_xticklabels(g.ax_heatmap.get_xticklabels(), fontsize=7.5)
    g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_yticklabels(), fontsize=7)
    g.fig.suptitle(f'Top 50 Differentially Expressed Genes: {c_name.replace("_", " ")}\n(Hierarchical Clustering of 49 Samples, Row Z-Score)',
                   fontsize=13, fontweight='bold', y=0.98)
                   
    for label, color in group_colors.items():
        g.ax_col_dendrogram.bar(0, 0, color=color, label=label, linewidth=0)
    g.ax_col_dendrogram.legend(loc="upper left", ncol=1, frameon=True, fontsize=9, bbox_to_anchor=(0.0, 1.35))
    
    heatmap_out1 = os.path.join(BASE_DIR, f"deg_outputs/figures\Heatmap_Top50_{c_name}.png")
    heatmap_out2 = os.path.join(BASE_DIR, f"Heatmap_Top50_{c_name}.png")
    g.savefig(heatmap_out1, dpi=300)
    g.savefig(heatmap_out2, dpi=300)
    plt.close(g.fig)
    print(f"Saved Top 50 Heatmap: {heatmap_out1}")

# -------------------------------------------------------------------------
# INVESTIGATE CLINICAL ASSOCIATIONS (TNM STAGE & HISTOLOGY)
# -------------------------------------------------------------------------
print("\nInvestigating clinical associations among CANCER samples (N=24)...")
cancer_meta = meta_df[meta_df['Sample_Group'] == 'CANCER'].copy()
cancer_samples = cancer_meta['GEO_Accession'].tolist()
cancer_expr = expr_exp[cancer_samples]

# Check TNM stages
# pT2aN0M0, pT3N0M0, pT3N1M0, pT3N2M0, pT3N3M0, pT3N2M1, pT3N3M1, pT4N0M0
# Classify into: Early/Localized (N0 M0, N=7), Lymph Node Positive (N+ M0, N=13), Distant Metastatic (M1, N=4)
def classify_stage(s):
    if 'M1' in s:
        return 'Metastatic_M1'
    elif 'N0' in s:
        return 'Localized_N0M0'
    else:
        return 'NodePositive_NplusM0'

# Extract stage string from Characteristics
stage_series = []
for idx, r in cancer_meta.iterrows():
    chars = r['Characteristics']
    stage_match = [c for c in chars.split(' | ') if c.startswith('cancer stage: ')]
    if stage_match:
        stage_series.append(stage_match[0].replace('cancer stage: ', ''))
    else:
        stage_series.append('Unknown')

cancer_meta['TNM_Stage'] = stage_series
cancer_meta['Stage_Category'] = cancer_meta['TNM_Stage'].apply(classify_stage)
print("Cancer samples by stage category:")
print(cancer_meta['Stage_Category'].value_counts())

# Save Clinical Subgroup Summary Table
cancer_meta_out = os.path.join(BASE_DIR, r"deg_outputs/tables\Cancer_Clinical_Subgroups.csv")
cancer_meta[['GEO_Accession', 'Title', 'TNM_Stage', 'Stage_Category', 'Characteristics']].to_csv(cancer_meta_out, index=False)
print(f"Saved Cancer Clinical Subgroups to: {cancer_meta_out}")

print("\nDifferential Expression and Clinical Investigation completed successfully!")