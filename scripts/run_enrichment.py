import os
import json
import requests
import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'scripts':
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
elif os.path.basename(SCRIPT_DIR) == '12_Real_GSE17154_Analysis':
    BASE_DIR = SCRIPT_DIR
else:
    BASE_DIR = os.path.join(SCRIPT_DIR, '12_Real_GSE17154_Analysis')

base_dir = BASE_DIR

print("================================================================================")
print("STAGE 5: GENE ONTOLOGY, KEGG AND REACTOME PATHWAY ENRICHMENT ANALYSIS")
print("================================================================================")

# Paths
deg_cancer_pn_path = os.path.join(base_dir, "results", "DEG", "DEG_Cancer_vs_PN_Top_FDR05_FC2.csv")
deg_full_path = os.path.join(base_dir, "results", "DEG", "DEG_Cancer_vs_PN_Full.csv")
annot_path = os.path.join(base_dir, "data", "annotation", "Probe_Annotation.csv")

deg_top_df = pd.read_csv(deg_cancer_pn_path)
deg_full_df = pd.read_csv(deg_full_path)
annot_df = pd.read_csv(annot_path)

# Background universe: All experimental, uniquely measured human genes on GPL6699
exp_annot = annot_df[annot_df['Is_Control'] == False]
universe_genes = set(exp_annot['Gene_Symbol'].dropna().unique())
universe_genes.discard('Unmapped')
print(f"Background Gene Universe: {len(universe_genes):,} unique genes from GPL6699")

# Significant DEGs (Cancer vs Paired Normal)
sig_degs = deg_top_df[deg_top_df['Gene_Symbol'] != 'Unmapped']
sig_gene_symbols = list(set(sig_degs['Gene_Symbol'].dropna().unique()))
print(f"Total Unique Significant DEGs (|Log2FC| >= 1.0 & FDR < 0.05): {len(sig_gene_symbols):,}")

# Function to query Enrichr using requests
ENRICHR_URL = 'https://maayanlab.cloud/Enrichr'

def query_enrichr_api(gene_list, description="GSE17154_DEGs"):
    genes_str = '\n'.join(gene_list)
    payload = {
        'list': (None, genes_str),
        'description': (None, description)
    }
    r = requests.post(f"{ENRICHR_URL}/addList", files=payload, timeout=25)
    r.raise_for_status()
    resp = r.json()
    return resp['userListId']

def get_enrichr_results_api(user_list_id, library_name):
    url = f"{ENRICHR_URL}/enrich?userListId={user_list_id}&backgroundType={library_name}"
    r = requests.get(url, timeout=25)
    r.raise_for_status()
    data = r.json()
    
    rows = []
    for item in data.get(library_name, []):
        term = item[1]
        pval = item[2]
        comb_score = item[4]
        genes = "; ".join(item[5])
        overlap_cnt = len(item[5])
        padj = item[6]
        
        rows.append({
            'Term': term,
            'Overlap_Count': overlap_cnt,
            'P_Value': pval,
            'Adj_P_Value': padj,
            'Combined_Score': comb_score,
            'Genes': genes
        })
    df = pd.DataFrame(rows)
    return df

print("\nSubmitting DEG list to Enrichr database...")
user_list_id = query_enrichr_api(sig_gene_symbols, description="GSE17154_Gastric_Cancer_DEGs")
print(f"Enrichr User List ID: {user_list_id}")

libraries = {
    'GO_BP': ('GO_Biological_Process_2021', 'GO_BP_Enrichment.csv'),
    'GO_MF': ('GO_Molecular_Function_2021', 'GO_MF_Enrichment.csv'),
    'GO_CC': ('GO_Cellular_Component_2021', 'GO_CC_Enrichment.csv'),
    'KEGG': ('KEGG_2021_Human', 'KEGG_Enrichment.csv'),
    'Reactome': ('Reactome_2022', 'Reactome_Enrichment.csv')
}

results_dict = {}

for cat, (lib, fname) in libraries.items():
    print(f"Retrieving enrichment for {cat} ({lib})...")
    res_df = get_enrichr_results_api(user_list_id, lib)
    
    out1 = os.path.join(base_dir, "results", "Enrichment", fname)
    out2 = os.path.join(base_dir, fname)
    res_df.to_csv(out1, index=False)
    res_df.to_csv(out2, index=False)
    results_dict[cat] = res_df
    
    sig_terms = res_df[res_df['Adj_P_Value'] < 0.05]
    print(f" -> {cat}: {len(res_df)} total terms tested | {len(sig_terms)} significant (FDR < 0.05)")

# -------------------------------------------------------------------------
# GENERATE PUBLICATION-QUALITY ENRICHMENT DOT PLOTS
# -------------------------------------------------------------------------
print("\nGenerating Enrichment Dot Plots...")

def plot_enrichment_dotplot(df, title, out_png, top_n=12):
    plot_df = df.head(top_n).copy()
    if len(plot_df) == 0:
        return
    plot_df['Clean_Term'] = plot_df['Term'].apply(lambda x: x.split(' (GO:')[0] if ' (GO:' in x else x)
    plot_df['Clean_Term'] = plot_df['Clean_Term'].apply(lambda x: x[:55] + '...' if len(x) > 55 else x)
    plot_df['-log10(FDR)'] = -np.log10(np.maximum(plot_df['Adj_P_Value'], 1e-30))
    plot_df = plot_df.sort_values(by='-log10(FDR)', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    scatter = ax.scatter(
        plot_df['-log10(FDR)'],
        plot_df['Clean_Term'],
        s=plot_df['Overlap_Count'] * 20 + 60,
        c=plot_df['-log10(FDR)'],
        cmap='viridis',
        edgecolors='black',
        linewidth=0.8,
        alpha=0.85
    )
    
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.7)
    cbar.set_label(r'$-\log_{10}(\mathrm{FDR})$', fontsize=11, fontweight='bold')
    
    ax.set_xlabel(r'$-\log_{10}(\mathrm{Adjusted\ p\text{-}value})$', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    fig.savefig(out_png, dpi=300)
    fig_name = os.path.basename(out_png)
    fig.savefig(os.path.join(base_dir, "figures", fig_name), dpi=300)
    plt.close(fig)
    print(f"Saved Dotplot: {out_png}")

plot_enrichment_dotplot(
    results_dict['GO_BP'],
    'Gene Ontology: Biological Process Enrichment\n(GSE17154 Gastric Cancer vs Paired Normal)',
    os.path.join(base_dir, "results", "Enrichment", "GO_BP_Enrichment_DotPlot.png")
)
plot_enrichment_dotplot(
    results_dict['GO_MF'],
    'Gene Ontology: Molecular Function Enrichment\n(GSE17154 Gastric Cancer vs Paired Normal)',
    os.path.join(base_dir, "results", "Enrichment", "GO_MF_Enrichment_DotPlot.png")
)
plot_enrichment_dotplot(
    results_dict['GO_CC'],
    'Gene Ontology: Cellular Component Enrichment\n(GSE17154 Gastric Cancer vs Paired Normal)',
    os.path.join(base_dir, "results", "Enrichment", "GO_CC_Enrichment_DotPlot.png")
)
plot_enrichment_dotplot(
    results_dict['KEGG'],
    'KEGG Pathway Enrichment\n(GSE17154 Gastric Cancer vs Paired Normal)',
    os.path.join(base_dir, "results", "Enrichment", "KEGG_Pathway_Enrichment_DotPlot.png")
)
plot_enrichment_dotplot(
    results_dict['Reactome'],
    'Reactome Pathway Enrichment\n(GSE17154 Gastric Cancer vs Paired Normal)',
    os.path.join(base_dir, "results", "Enrichment", "Reactome_Pathway_Enrichment_DotPlot.png")
)

# -------------------------------------------------------------------------
# FAST VECTORIZED RANKED GENE-SET ENRICHMENT ANALYSIS (GSEA)
# -------------------------------------------------------------------------
print("\nPerforming Fast Ranked Gene-Set Enrichment Analysis (GSEA)...")
ranked_genes = deg_full_df[deg_full_df['Gene_Symbol'] != 'Unmapped'].copy()
ranked_genes['abs_t'] = ranked_genes['Moderated_t'].abs()
idx_max = ranked_genes.groupby('Gene_Symbol')['abs_t'].idxmax()
ranked_unique = ranked_genes.loc[idx_max].sort_values(by='Moderated_t', ascending=False)
N_total = len(ranked_unique)
print(f"Ranked gene universe for GSEA: {N_total:,} genes")

all_indices = np.arange(N_total)
gene_ranks = {g: r for r, g in enumerate(ranked_unique['Gene_Symbol'])}
top_pathways = list(results_dict['KEGG'].head(20)['Term']) + list(results_dict['Reactome'].head(20)['Term'])

gsea_records = []
for p_term in top_pathways:
    kegg_row = results_dict['KEGG'][results_dict['KEGG']['Term'] == p_term]
    react_row = results_dict['Reactome'][results_dict['Reactome']['Term'] == p_term]
    genes_in_term = []
    if len(kegg_row) > 0:
        genes_in_term = kegg_row.iloc[0]['Genes'].split('; ')
    elif len(react_row) > 0:
        genes_in_term = react_row.iloc[0]['Genes'].split('; ')
        
    term_ranks = np.array([gene_ranks[g] for g in genes_in_term if g in gene_ranks], dtype=int)
    if len(term_ranks) >= 3:
        mask = np.ones(N_total, dtype=bool)
        mask[term_ranks] = False
        other_ranks = all_indices[mask]
        
        stat, pval = stats.mannwhitneyu(term_ranks, other_ranks, alternative='two-sided')
        mean_rank = float(np.mean(term_ranks))
        median_rank = float(np.median(term_ranks))
        direction = "Up-regulated (Shifted to Top)" if mean_rank < N_total/2 else "Down-regulated (Shifted to Bottom)"
        gsea_records.append({
            'Pathway': p_term,
            'Gene_Count': len(term_ranks),
            'Mean_Rank': mean_rank,
            'Median_Rank': median_rank,
            'Direction': direction,
            'MannWhitney_P_Value': pval
        })

gsea_df = pd.DataFrame(gsea_records)
if len(gsea_df) > 0:
    reject, padj, _, _ = multipletests(gsea_df['MannWhitney_P_Value'], method='fdr_bh')
    gsea_df['Adj_P_Value'] = padj
    gsea_df = gsea_df.sort_values(by='Adj_P_Value').reset_index(drop=True)
    gsea_out1 = os.path.join(base_dir, "results", "Enrichment", "GSEA_Results.csv")
    gsea_out2 = os.path.join(base_dir, "GSEA_Results.csv")
    gsea_df.to_csv(gsea_out1, index=False)
    gsea_df.to_csv(gsea_out2, index=False)
    print(f"Saved GSEA Results to: {gsea_out1}")
    print(gsea_df.head(5))

print("\nGene Ontology and Pathway Enrichment completed successfully!")
