import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'scripts':
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
elif os.path.basename(SCRIPT_DIR) == '12_Real_GSE17154_Analysis':
    BASE_DIR = SCRIPT_DIR
else:
    BASE_DIR = os.path.join(SCRIPT_DIR, '12_Real_GSE17154_Analysis')

import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

print("================================================================================")
print("STAGE 7: CLINICAL AND SUBGROUP EXPLORATORY ANALYSIS (CANCER N=24)")
print("================================================================================")

base_dir = BASE_DIR
meta_path = os.path.join(base_dir, "data", "metadata", "GSE17154_real_sample_metadata.csv")
subgroup_path = os.path.join(base_dir, "results", "DEG", "Cancer_Clinical_Subgroups.csv")

meta_df = pd.read_csv(meta_path)
sub_df = pd.read_csv(subgroup_path)

print(f"Total Cancer Samples analyzed: {len(sub_df)}")
print("\nTNM Stage Categories:")
print(sub_df['Stage_Category'].value_counts())

# Extract Nuclear Grade and Survival Followup from Characteristics
grades = []
outcomes = []
for idx, r in sub_df.iterrows():
    chars = r['Characteristics']
    parts = chars.split(' | ')
    g_val = 'Unknown'
    o_val = 'Unknown'
    for p in parts:
        if p.startswith('cancer nuclear grade: '):
            g_val = p.replace('cancer nuclear grade: ', '').strip()
        elif p.startswith('no evidence of disease (ned) or failed: '):
            o_val = p.replace('no evidence of disease (ned) or failed: ', '').strip()
    grades.append(g_val)
    outcomes.append(o_val)

sub_df['Nuclear_Grade'] = grades
sub_df['Clinical_Outcome'] = outcomes

print("\nNuclear Grade Breakdown:")
print(sub_df['Nuclear_Grade'].value_counts())
print("\nClinical Outcome Breakdown (NED vs Failed):")
print(sub_df['Clinical_Outcome'].value_counts())

# Save Detailed Clinical Table
sub_df.to_csv(os.path.join(base_dir, "results", "Clinical", "Cancer_Detailed_Clinical_Summary.csv"), index=False)
sub_df.to_csv(os.path.join(base_dir, "Cancer_Detailed_Clinical_Summary.csv"), index=False)

# -------------------------------------------------------------------------
# GENERATE CLINICAL SUBGROUP VISUALIZATION
# -------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# Plot 1: TNM Stage Distribution
stage_counts = sub_df['Stage_Category'].value_counts()
colors1 = ['#3F51B5', '#009688', '#E91E63']
stage_labels = [s.replace('_', ' ') for s in stage_counts.index]
ax1.bar(stage_labels, stage_counts.values, color=colors1, edgecolor='black', alpha=0.85, width=0.55)
ax1.set_ylabel('Sample Count (N)', fontsize=11, fontweight='bold')
ax1.set_title('Gastric Cancer Patients by Pathological Stage\n(GSE17154 Cancer Cohort N=24)', fontsize=12, fontweight='bold', pad=12)
ax1.set_ylim(0, 16)
for i, v in enumerate(stage_counts.values):
    ax1.text(i, v + 0.4, f"N={v}\n({v/24*100:.1f}%)", ha='center', fontsize=9.5, fontweight='bold')

# Plot 2: Clinical Outcome by Stage
cross_tab = pd.crosstab(sub_df['Stage_Category'], sub_df['Clinical_Outcome'])
cross_tab.index = [s.replace('_', ' ') for s in cross_tab.index]
cross_tab.plot(kind='bar', stacked=True, ax=ax2, colormap='Accent', edgecolor='black', alpha=0.85, width=0.55)
ax2.set_ylabel('Sample Count (N)', fontsize=11, fontweight='bold')
ax2.set_title('Disease Outcome (NED vs Failed) across Stages\n(GSE17154 Cancer Cohort N=24)', fontsize=12, fontweight='bold', pad=12)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0, fontsize=10)
ax2.legend(title='Clinical Outcome', fontsize=9, loc='upper right')
ax2.set_ylim(0, 16)

plt.tight_layout()
fig_out1 = os.path.join(base_dir, "results", "Clinical", "Clinical_Subgroups_Distribution.png")
fig_out2 = os.path.join(base_dir, "figures", "Clinical_Subgroups_Distribution.png")
fig_out3 = os.path.join(base_dir, "Clinical_Subgroups_Distribution.png")
fig.savefig(fig_out1, dpi=300)
fig.savefig(fig_out2, dpi=300)
fig.savefig(fig_out3, dpi=300)
plt.close(fig)

print(f"Saved Clinical Subgroup figure to: {fig_out1}")
print("Clinical Subgroup Analysis completed successfully!")
