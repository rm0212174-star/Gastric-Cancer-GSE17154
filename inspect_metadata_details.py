import pandas as pd

df = pd.read_csv(r"12_Real_GSE17154_Analysis\metadata\GSE17154_real_sample_metadata.csv")
print("Total samples:", len(df))
print("\nGroup value counts:")
print(df['Sample_Group'].value_counts())

cancer_df = df[df['Sample_Group'] == 'CANCER']
print(f"\n--- CANCER SAMPLES ({len(cancer_df)}) ---")
for idx, r in cancer_df.iterrows():
    print(f"{r['GEO_Accession']} | {r['Title']} | {r['Characteristics']}")

pn_df = df[df['Sample_Group'] == 'Paired_Normal_PN']
print(f"\n--- PN SAMPLES ({len(pn_df)}) ---")
for idx, r in pn_df.iterrows():
    print(f"{r['GEO_Accession']} | {r['Title']} | {r['Characteristics']}")

an_df = df[df['Sample_Group'] == 'Apparently_Normal_AN']
print(f"\n--- AN SAMPLES ({len(an_df)}) ---")
for idx, r in an_df.iterrows():
    print(f"{r['GEO_Accession']} | {r['Title']} | {r['Characteristics']}")
