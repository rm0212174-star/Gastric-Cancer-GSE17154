import pandas as pd
import os

BASE_DIR = r"C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis"
annot_path = os.path.join(BASE_DIR, "data", "annotation", "Probe_Annotation.csv")

df = pd.read_csv(annot_path)

# 1. GPL6699_VERIFIED_ANNOTATION.csv
ver_path = os.path.join(BASE_DIR, "GPL6699_VERIFIED_ANNOTATION.csv")
df.to_csv(ver_path, index=False)

# 2. PROBE_TO_GENE_MAPPING.csv (experimental probes only)
exp_df = df[~df["Is_Control"]].copy()
mapping_df = exp_df[["Probe_ID", "Reporter_Name", "Gene_Symbol", "Gene_Description", "CompositeSequence_ID", "GC_Content"]]
map_path = os.path.join(BASE_DIR, "PROBE_TO_GENE_MAPPING.csv")
mapping_df.to_csv(map_path, index=False)

# 3. GENE_MAPPING_STATISTICS.csv
gene_counts = exp_df["Gene_Symbol"].value_counts()
stat_summary = pd.DataFrame({
    "Metric": [
        "Total_Array_Features",
        "Technical_Control_Spots",
        "Experimental_Probes",
        "Unique_Gene_Symbols",
        "Single_Probe_Genes",
        "Multi_Probe_Genes",
        "Max_Probes_For_Single_Gene",
        "Gene_With_Max_Probes"
    ],
    "Value": [
        len(df),
        df["Is_Control"].sum(),
        len(exp_df),
        len(gene_counts),
        (gene_counts == 1).sum(),
        (gene_counts > 1).sum(),
        gene_counts.max(),
        gene_counts.index[0]
    ]
})
stat_path = os.path.join(BASE_DIR, "GENE_MAPPING_STATISTICS.csv")
stat_summary.to_csv(stat_path, index=False)

print("Stage 3 CSV deliverables generated successfully:")
print(stat_summary)
