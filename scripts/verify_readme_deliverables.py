import os
import re

readme_path = r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis\README.md"
base_dir = r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis"

with open(readme_path, "r", encoding="utf-8") as f:
    text = f.read()

# Check figures mentioned
fig_matches = re.findall(r"([A-Za-z0-9_\-]+\.png)", text)
fig_matches = list(set(fig_matches))

print(f"Figures mentioned in README: {len(fig_matches)}")
for fig in sorted(fig_matches):
    # search in base_dir, base_dir/figures, base_dir/results/figures
    found = False
    for loc in [base_dir, os.path.join(base_dir, "figures"), os.path.join(base_dir, "results", "figures")]:
        if os.path.exists(os.path.join(loc, fig)):
            found = True
            break
    print(f"  {fig}: {'EXISTS' if found else 'MISSING'}")

# Check tables mentioned
tab_matches = re.findall(r"([A-Za-z0-9_\-]+\.csv)", text)
tab_matches = list(set(tab_matches))
print(f"\nTables mentioned in README: {len(tab_matches)}")
for tab in sorted(tab_matches):
    found = False
    for loc in [base_dir, os.path.join(base_dir, "results", "tables"), os.path.join(base_dir, "deg_outputs", "tables"), os.path.join(base_dir, "data", "metadata"), os.path.join(base_dir, "data", "processed_matrix"), os.path.join(base_dir, "data", "annotation")]:
        if os.path.exists(os.path.join(loc, tab)):
            found = True
            break
    print(f"  {tab}: {'EXISTS' if found else 'MISSING'}")
