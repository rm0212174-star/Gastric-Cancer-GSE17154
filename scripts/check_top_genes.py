import os
import pandas as pd

base = r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis"
t1 = pd.read_csv(os.path.join(base, "results", "tables", "DEG_Cancer_vs_PN_Gene_Level_Strict_FDR05_FC2.csv"))
t2 = pd.read_csv(os.path.join(base, "results", "tables", "DEG_Cancer_vs_AN_Gene_Level_Strict_FDR05_FC2.csv"))

print(f"Cancer vs PN genes: {len(t1)}")
for g in ['SSPO', 'NNAT', 'P15RS', 'CLU', 'ATP1B4', 'KLRA1', 'GAPDH']:
    sub = t1[t1['Gene_Symbol'] == g]
    if not sub.empty:
        r = sub.iloc[0]
        print(f"  {g}: Log2FC={r['Log2FC']:.3f}, Mod_t={r['Moderated_t']:.3f}, FDR={r['Adj_P_Value']:.2e}")
    else:
        print(f"  {g}: Not in strict table")
