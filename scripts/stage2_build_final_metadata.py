import pandas as pd
import os

BASE_DIR = r"C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis"
meta_raw_path = os.path.join(BASE_DIR, "metadata", "GSE17154_real_sample_metadata.csv")
clinical_path = os.path.join(BASE_DIR, "Cancer_Detailed_Clinical_Summary.csv")

df_meta = pd.read_csv(meta_raw_path)
df_clin = pd.read_csv(clinical_path)

# Map clinical columns into full metadata
clin_dict = df_clin.set_index("GEO_Accession").to_dict(orient="index")

final_rows = []
for idx, row in df_meta.iterrows():
    geo_id = row["GEO_Accession"]
    title = row["Title"]
    grp = row["Sample_Group"]
    
    # Tissue origin description vs statistical group
    if grp == "CANCER":
        tissue_origin = "Primary Gastric Tumor"
        stat_group = "CANCER"
        c_info = clin_dict.get(geo_id, {})
        tnm = c_info.get("TNM_Stage", "Unknown")
        stage_cat = c_info.get("Stage_Category", "Unknown")
        grade = c_info.get("Nuclear_Grade", "Unknown")
        outcome = c_info.get("Clinical_Outcome", "Unknown")
        hpe = "Adenocarcinoma" if "Adenocarcinoma" in str(row["Characteristics"]) else ("Neuroendocrine" if "Neuro" in str(row["Characteristics"]) else "Unknown")
    elif grp == "Paired_Normal_PN":
        tissue_origin = "Non-tumorous Gastric Mucosa from Cancer Stomach"
        stat_group = "Paired_Normal_PN"
        tnm = "N/A (Non-tumorous)"
        stage_cat = "Normal_Mucosa"
        grade = "N/A"
        outcome = "N/A"
        hpe = "Histologically Normal"
    else: # Apparently_Normal_AN
        tissue_origin = "Apparently Normal Gastric Mucosa from Healthy Endoscopy Control"
        stat_group = "Apparently_Normal_AN"
        tnm = "N/A (Healthy Control)"
        stage_cat = "Healthy_Control"
        grade = "N/A"
        outcome = "N/A"
        hpe = "Endoscopically Normal"
        
    final_rows.append({
        "Sample_ID": geo_id,
        "GEO_Title": title,
        "Statistical_Group": stat_group,
        "Tissue_Origin": tissue_origin,
        "Organism": "Homo sapiens",
        "Microarray_Platform": "GPL6699",
        "Dye_Cy5_Sample": "Patient Tissue RNA",
        "Dye_Cy3_Reference": "Stratagene UHRR",
        "Histopathology": hpe,
        "TNM_Stage": tnm,
        "Stage_Category": stage_cat,
        "Nuclear_Grade": grade,
        "Clinical_Outcome": outcome,
        "Statistical_Pairing_Status": "Unpaired (No verified 1-to-1 patient ID in public GEO)"
    })

df_final = pd.DataFrame(final_rows)
out_csv = os.path.join(BASE_DIR, "FINAL_SAMPLE_METADATA.csv")
df_final.to_csv(out_csv, index=False)
df_final.to_csv(os.path.join(BASE_DIR, "metadata", "FINAL_SAMPLE_METADATA.csv"), index=False)
print(f"Generated {out_csv} with {len(df_final)} samples.")
print(df_final["Statistical_Group"].value_counts())
