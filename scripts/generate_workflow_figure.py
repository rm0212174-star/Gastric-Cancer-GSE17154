import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'scripts':
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
elif os.path.basename(SCRIPT_DIR) == '12_Real_GSE17154_Analysis':
    BASE_DIR = SCRIPT_DIR
else:
    BASE_DIR = os.path.join(SCRIPT_DIR, '12_Real_GSE17154_Analysis')

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

print("Generating Study Workflow Schematic Diagram...")
fig, ax = plt.subplots(figsize=(12, 8))

# Define workflow boxes
boxes = [
    ("1. Public Data Acquisition\n(NCBI GEO GSE17154)", 0.5, 0.88, "#BBDEFB"),
    ("Two-Colour Microarray (GPL6699, Agilent 4x44K)\nCy5: Patient Gastric Tissue | Cy3: Stratagene UHRR\n49 Clinical Samples: Cancer (24), PN (20), AN (5)", 0.5, 0.77, "#E3F2FD"),
    ("2. Rigorous Quality Control & GPL6699 Annotation", 0.5, 0.63, "#C8E6C9"),
    ("44,544 Total Probes -> 4,347 Controls Excluded\n40,197 Experimental Probes (25,518 Unique Human Genes)\nBoxplots, Density Curves, Sample Pearson Correlation (r=0.61), PCA", 0.5, 0.52, "#E8F8F5"),
    ("3. Differential Expression Analysis (limma)", 0.5, 0.38, "#FFE0B2"),
    ("Unpaired 3-Group Linear Model (~ 0 + Group)\nEmpirical Bayes Moderation & Benjamini-Hochberg FDR\nCancer vs PN: 633 DEGs | Cancer vs AN: 643 DEGs | PN vs AN: 0 DEGs", 0.5, 0.27, "#FFF3E0"),
    ("4. Systems Biology & Clinical Investigation", 0.5, 0.13, "#D1C4E9"),
    ("GO (BP, MF, CC), KEGG, Reactome Enrichment & Ranked GSEA\nSTRING v12.5 PPI Network (Hubs: GAPDH, ACTB, CSF3, LTF, CTSD)\nPathological TNM Stage Stratification (Localized, Node+, Metastatic)", 0.5, 0.02, "#EDE7F6")
]

for title, x, y, color in boxes:
    is_header = "1." in title or "2." in title or "3." in title or "4." in title
    h = 0.07 if is_header else 0.08
    w = 0.85
    rect = patches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.2, edgecolor="black" if is_header else "gray", facecolor=color, alpha=0.95
    )
    ax.add_patch(rect)
    ax.text(x, y, title, ha='center', va='center',
            fontsize=10.5 if is_header else 9.5,
            fontweight='bold' if is_header else 'normal', color='black')

# Draw arrows between steps
arrows = [(0.73, 0.67), (0.48, 0.42), (0.23, 0.17)]
for y_start, y_end in arrows:
    ax.annotate('', xy=(0.5, y_end), xytext=(0.5, y_start),
                arrowprops=dict(facecolor='black', edgecolor='black', width=1.5, headwidth=8, shrink=0.05))

ax.set_xlim(0, 1)
ax.set_ylim(-0.04, 0.96)
ax.axis('off')
ax.set_title("GSE17154 Gastric Cancer Bioinformatics Research Workflow",
             fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
base_dir = BASE_DIR
fig.savefig(os.path.join(base_dir, "figures", "Study_Workflow_Diagram.png"), dpi=300)
fig.savefig(os.path.join(base_dir, "Study_Workflow_Diagram.png"), dpi=300)
plt.close(fig)
print("Saved Study_Workflow_Diagram.png")
