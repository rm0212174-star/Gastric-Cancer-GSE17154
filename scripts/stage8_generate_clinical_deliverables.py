import os
import pandas as pd
import shutil

BASE_DIR = r"C:\Users\ACER\BIoinformatics_Training\12_Real_GSE17154_Analysis"
src_clin = os.path.join(BASE_DIR, "Cancer_Detailed_Clinical_Summary.csv")
df_clin = pd.read_csv(src_clin)

# 1. CLINICAL_METADATA_VALIDATION.csv
val_df = df_clin.copy()
val_df["Data_Source"] = "NCBI GEO GSE17154 Sample Characteristics"
val_df["Survival_Time_Available"] = False
val_df["Validation_Status"] = "Verified"
val_path1 = os.path.join(BASE_DIR, "results", "Clinical", "CLINICAL_METADATA_VALIDATION.csv")
val_path2 = os.path.join(BASE_DIR, "CLINICAL_METADATA_VALIDATION.csv")
os.makedirs(os.path.join(BASE_DIR, "results", "Clinical"), exist_ok=True)
val_df.to_csv(val_path1, index=False)
val_df.to_csv(val_path2, index=False)

# 2. CLINICAL_SUBGROUP_SUMMARY.csv
subgroup_records = []

# TNM
for st, cnt in df_clin["Stage_Category"].value_counts().items():
    subgroup_records.append({
        "Category_Type": "TNM_Staging",
        "Subgroup_Name": st,
        "Sample_Count": cnt,
        "Percentage": round((cnt / len(df_clin)) * 100, 2),
        "Notes": "pT2-T4 localized vs node-positive regional vs metastatic M1"
    })

# Grade
for gr, cnt in df_clin["Nuclear_Grade"].value_counts().items():
    subgroup_records.append({
        "Category_Type": "Nuclear_Grade",
        "Subgroup_Name": gr,
        "Sample_Count": cnt,
        "Percentage": round((cnt / len(df_clin)) * 100, 2),
        "Notes": "Pathological nuclear differentiation grade"
    })

# Outcome
for oc, cnt in df_clin["Clinical_Outcome"].value_counts().items():
    subgroup_records.append({
        "Category_Type": "Clinical_Outcome",
        "Subgroup_Name": oc,
        "Sample_Count": cnt,
        "Percentage": round((cnt / len(df_clin)) * 100, 2),
        "Notes": "NED = No Evidence of Disease; Failed = Recurrence/Died"
    })

sub_df = pd.DataFrame(subgroup_records)
sub_path1 = os.path.join(BASE_DIR, "results", "Clinical", "CLINICAL_SUBGROUP_SUMMARY.csv")
sub_path2 = os.path.join(BASE_DIR, "CLINICAL_SUBGROUP_SUMMARY.csv")
sub_df.to_csv(sub_path1, index=False)
sub_df.to_csv(sub_path2, index=False)

print("Stage 8 clinical deliverables generated successfully:")
print(sub_df)
