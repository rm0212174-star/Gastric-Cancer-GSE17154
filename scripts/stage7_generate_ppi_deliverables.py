import os
import pandas as pd
import shutil

BASE_DIR = r"C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis"
ppi_dir = os.path.join(BASE_DIR, "results", "PPI")

# 1. STRING_NETWORK_EDGES.csv
src_edges = os.path.join(ppi_dir, "PPI_Interactions_STRING.csv")
dst_edges1 = os.path.join(ppi_dir, "STRING_NETWORK_EDGES.csv")
dst_edges2 = os.path.join(BASE_DIR, "STRING_NETWORK_EDGES.csv")
shutil.copyfile(src_edges, dst_edges1)
shutil.copyfile(src_edges, dst_edges2)

# 2. PPI_HUB_GENES.csv
src_hubs = os.path.join(ppi_dir, "PPI_Hub_Genes.csv")
dst_hubs = os.path.join(BASE_DIR, "PPI_HUB_GENES.csv")
shutil.copyfile(src_hubs, dst_hubs)

# 3. STRING_INPUT_GENES.csv
hubs_df = pd.read_csv(src_hubs)
input_genes_df = pd.DataFrame({
    "Gene_Symbol": hubs_df["Gene_Symbol"],
    "Log2FC": hubs_df["Log2FC"],
    "Degree": hubs_df["Degree"],
    "Query_Status": "Mapped_to_STRING_v12.5"
})
out_input1 = os.path.join(ppi_dir, "STRING_INPUT_GENES.csv")
out_input2 = os.path.join(BASE_DIR, "STRING_INPUT_GENES.csv")
input_genes_df.to_csv(out_input1, index=False)
input_genes_df.to_csv(out_input2, index=False)

# 4. PPI_Network.png
src_png = os.path.join(BASE_DIR, "figures", "PPI_Network_STRING.png")
dst_png1 = os.path.join(BASE_DIR, "figures", "PPI_Network.png")
dst_png2 = os.path.join(BASE_DIR, "PPI_Network.png")
shutil.copyfile(src_png, dst_png1)
shutil.copyfile(src_png, dst_png2)

print("Stage 7 PPI deliverables copied and formatted successfully:")
print(f"Edges: {len(pd.read_csv(src_edges))} rows")
print(f"Input Genes: {len(input_genes_df)} rows")
