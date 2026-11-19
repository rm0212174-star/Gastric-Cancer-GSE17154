import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'scripts':
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
elif os.path.basename(SCRIPT_DIR) == '12_Real_GSE17154_Analysis':
    BASE_DIR = SCRIPT_DIR
else:
    BASE_DIR = os.path.join(SCRIPT_DIR, '12_Real_GSE17154_Analysis')

import os
import json
import subprocess
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("================================================================================")
print("STAGE 6: PROTEIN-PROTEIN INTERACTION (PPI) NETWORK ANALYSIS (STRING v12.5)")
print("================================================================================")

base_dir = BASE_DIR
deg_top_path = os.path.join(base_dir, "results", "DEG", "DEG_Cancer_vs_PN_Top_FDR05_FC2.csv")
deg_top_df = pd.read_csv(deg_top_path)

# Select top candidate DEGs ranked by significance
top_degs = deg_top_df[deg_top_df['Gene_Symbol'] != 'Unmapped'].head(60).copy()
unique_genes = top_degs['Gene_Symbol'].dropna().unique().tolist()
# Filter out non-alphanumeric identifiers (like suid=...)
valid_genes = [g for g in unique_genes if not g.startswith('suid=') and not g.startswith('LOC') and len(g) > 1][:45]
print(f"Querying STRING v12.5 for {len(valid_genes)} top candidate genes...")
print("Candidate genes:", ", ".join(valid_genes[:15]))

# Query STRING API using curl.exe
genes_query = "%0d".join(valid_genes)
url = f"https://string-db.org/api/json/network?identifiers={genes_query}&species=9606&required_score=400"

curl_cmd = ["curl.exe", "-s", url]
proc = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
raw_json = proc.stdout

interactions = json.loads(raw_json)
print(f"STRING API returned {len(interactions)} protein interaction edges (confidence >= 0.400).")

# Parse interactions into DataFrame
edges = []
for item in interactions:
    edges.append({
        'Protein_A': item['preferredName_A'],
        'Protein_B': item['preferredName_B'],
        'StringId_A': item['stringId_A'],
        'StringId_B': item['stringId_B'],
        'Combined_Score': item['score'],
        'Experimental_Score': item['escore'],
        'Database_Score': item['dscore'],
        'Textmining_Score': item['tscore']
    })

edges_df = pd.DataFrame(edges)
edges_out1 = os.path.join(base_dir, "results", "PPI", "PPI_Interactions_STRING.csv")
edges_out2 = os.path.join(base_dir, "PPI_Interactions_STRING.csv")
edges_df.to_csv(edges_out1, index=False)
edges_df.to_csv(edges_out2, index=False)
print(f"Saved PPI interactions to: {edges_out1}")

# Construct NetworkX Graph
G = nx.Graph()
# Add all valid candidate genes as nodes
for g in valid_genes:
    # Find logFC
    match = top_degs[top_degs['Gene_Symbol'] == g]
    lfc = match.iloc[0]['Log2FC'] if len(match) > 0 else 0.0
    G.add_node(g, logFC=lfc)

# Add edges
for idx, r in edges_df.iterrows():
    G.add_edge(r['Protein_A'], r['Protein_B'], weight=r['Combined_Score'])

print(f"\nPPI Graph summary: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Compute Centrality Metrics
degrees = dict(G.degree())
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)

node_metrics = []
for node in G.nodes():
    node_metrics.append({
        'Gene_Symbol': node,
        'Log2FC': G.nodes[node].get('logFC', 0.0),
        'Degree': degrees[node],
        'Betweenness_Centrality': betweenness[node],
        'Closeness_Centrality': closeness[node],
        'Is_Connected': degrees[node] > 0
    })

nodes_df = pd.DataFrame(node_metrics).sort_values(by=['Degree', 'Betweenness_Centrality'], ascending=False).reset_index(drop=True)
nodes_out1 = os.path.join(base_dir, "results", "PPI", "PPI_Hub_Genes.csv")
nodes_out2 = os.path.join(base_dir, "PPI_Hub_Genes.csv")
nodes_df.to_csv(nodes_out1, index=False)
nodes_df.to_csv(nodes_out2, index=False)

print("\n--- Candidate Hub Genes Identified ---")
print(nodes_df.head(10))

# -------------------------------------------------------------------------
# GENERATE NETWORK VISUALIZATION
# -------------------------------------------------------------------------
print("\nGenerating PPI Network Visualization...")
fig, ax = plt.subplots(figsize=(12, 10))

# Connected subgraph for clean layout
connected_nodes = [n for n in G.nodes() if degrees[n] > 0]
if len(connected_nodes) > 0:
    H = G.subgraph(connected_nodes)
    pos = nx.spring_layout(H, k=0.55, seed=42)
    
    node_colors = ['#E53935' if H.nodes[n].get('logFC', 0) > 0 else '#1E88E5' for n in H.nodes()]
    node_sizes = [degrees[n] * 350 + 600 for n in H.nodes()]
    
    nx.draw_networkx_nodes(H, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9,
                           edgecolors='black', linewidths=1.2, ax=ax)
    
    edge_weights = [H[u][v]['weight'] * 3.0 for u, v in H.edges()]
    nx.draw_networkx_edges(H, pos, width=edge_weights, alpha=0.6, edge_color='gray', ax=ax)
    
    labels = {n: f"{n}\n(deg={degrees[n]})" for n in H.nodes()}
    nx.draw_networkx_labels(H, pos, labels=labels, font_size=9, font_weight='bold', font_color='black', ax=ax)
else:
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, ax=ax, with_labels=True)

ax.set_title("Protein-Protein Interaction (PPI) Network of Candidate DEGs\n(STRING Database v12.5, Confidence Threshold >= 0.400)",
             fontsize=13, fontweight='bold', pad=15)
ax.axis('off')

# Custom legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Up-regulated in Cancer', markerfacecolor='#E53935', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Down-regulated in Cancer', markerfacecolor='#1E88E5', markersize=12),
    Line2D([0], [0], color='gray', lw=2, label='Confidence-weighted edge')
]
ax.legend(handles=legend_elements, loc='lower left', frameon=True, fontsize=10)
plt.tight_layout()

net_out1 = os.path.join(base_dir, "results", "PPI", "PPI_Network_STRING.png")
net_out2 = os.path.join(base_dir, "figures", "PPI_Network_STRING.png")
net_out3 = os.path.join(base_dir, "PPI_Network_STRING.png")
fig.savefig(net_out1, dpi=300)
fig.savefig(net_out2, dpi=300)
fig.savefig(net_out3, dpi=300)
plt.close(fig)

print(f"Saved PPI Network plot to: {net_out1}")
print("PPI Network Analysis completed successfully!")
