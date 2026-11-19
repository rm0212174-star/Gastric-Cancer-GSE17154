import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == 'scripts':
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
elif os.path.basename(SCRIPT_DIR) == '12_Real_GSE17154_Analysis':
    BASE_DIR = SCRIPT_DIR
else:
    BASE_DIR = os.path.join(SCRIPT_DIR, '12_Real_GSE17154_Analysis')

import gzip
import os
import pandas as pd
import numpy as np

print("================================================================================")
print("TASK 2: PARSING OFFICIAL GPL6699 SOFT ANNOTATION & GPR MAPPING")
print("================================================================================")

soft_path = os.path.join(BASE_DIR, r"raw_downloads\GPL6699_family.soft.gz")
gpr_path = os.path.join(BASE_DIR, r"raw_downloads\GSM429115.gpr.gz")

# 1. Read GPR spot-level annotations (44,544 rows)
print("Parsing GPR file for Spot-level Name and ID...")
gpr_spots = []
with gzip.open(gpr_path, 'rt', encoding='utf-8', errors='replace') as f:
    for i in range(23):
        f.readline()
    header = f.readline().strip().split('\t')
    id_idx = header.index('ID')
    name_idx = header.index('Name')
    b_idx = header.index('Block')
    c_idx = header.index('Column')
    r_idx = header.index('Row')
    
    for line in f:
        parts = line.strip().split('\t')
        gpr_spots.append({
            'Block': parts[b_idx],
            'Column': parts[c_idx],
            'Row': parts[r_idx],
            'GPR_ID': parts[id_idx],
            'GPR_Name': parts[name_idx].strip('"')
        })

print(f"Loaded {len(gpr_spots):,} spots from GPR.")

# 2. Read GPL6699 SOFT platform table (44,544 rows)
print("Parsing GPL6699 SOFT table...")
soft_probes = []
with gzip.open(soft_path, 'rt', encoding='utf-8', errors='replace') as f:
    in_table = False
    header = None
    for line in f:
        line_clean = line.rstrip('\r\n')
        if not in_table:
            if line_clean.startswith('!platform_table_begin'):
                in_table = True
        else:
            if line_clean.startswith('!platform_table_end'):
                break
            if header is None:
                header = line_clean.split('\t')
            else:
                parts = line_clean.split('\t')
                row_dict = dict(zip(header, parts))
                soft_probes.append(row_dict)

print(f"Loaded {len(soft_probes):,} probes from GPL6699 SOFT.")
assert len(gpr_spots) == len(soft_probes) == 44544, "Counts must match exactly 44,544"

# 3. Construct unified probe annotation table
annot_records = []
for i in range(44544):
    sp = gpr_spots[i]
    sf = soft_probes[i]
    
    probe_id = sf['ID']
    rep_name = sf.get('Reporter Name', '')
    role = sf.get('Reporter Group[role]', 'Experimental')
    ctrl_type = sf.get('Reporter ControlType', '')
    cs_id = sf.get('CompositeSequence Identifier', '')
    cs_name = sf.get('CompositeSequence Name', '')
    seq = sf.get('SEQUENCE', '')
    gc = sf.get('Reporter BioSequence [gcContent]', '')
    
    gpr_gene = sp['GPR_ID']
    gpr_desc = sp['GPR_Name']
    
    # Check if control probe
    is_control = (role == 'Control') or (ctrl_type != '') or (gpr_gene.lower() in ['empty', 'blank'])
    
    # Extract gene symbol and identifier
    gene_symbol = ""
    entrez_id = ""
    genbank_acc = ""
    unigene_id = ""
    
    # Determine gene symbol prioritizing GPR_ID if valid, or CS_ID
    if cs_id.startswith('URN:LSID:smd.stanford.edu:geneSymbol:'):
        symbol_from_cs = cs_id.replace('URN:LSID:smd.stanford.edu:geneSymbol:', '')
    elif cs_id.startswith('URN:LSID:smd.stanford.edu:locusLink:'):
        entrez_id = cs_id.replace('URN:LSID:smd.stanford.edu:locusLink:', '')
        symbol_from_cs = ""
    elif cs_id.startswith('URN:LSID:smd.stanford.edu:unigene:'):
        unigene_id = cs_id.replace('URN:LSID:smd.stanford.edu:unigene:', '')
        symbol_from_cs = ""
    elif cs_id.startswith('URN:LSID:smd.stanford.edu:genbank:'):
        genbank_acc = cs_id.replace('URN:LSID:smd.stanford.edu:genbank:', '')
        symbol_from_cs = ""
    elif cs_id.startswith('URN:LSID:smd.stanford.edu:embl:'):
        genbank_acc = cs_id.replace('URN:LSID:smd.stanford.edu:embl:', '')
        symbol_from_cs = ""
    else:
        symbol_from_cs = ""
        
    # GPR_ID has gene symbols (e.g. ACTB, RPL13A, ACSL6)
    if gpr_gene not in ['', 'empty', 'blank', '--', 'null', 'None']:
        gene_symbol = gpr_gene
    elif symbol_from_cs != "":
        gene_symbol = symbol_from_cs
    elif cs_name != "" and not cs_name.startswith('Hs.') and not cs_name.startswith('Random'):
        gene_symbol = cs_name

    annot_records.append({
        'Probe_ID': probe_id,
        'Reporter_Name': rep_name,
        'Role': role,
        'ControlType': ctrl_type if ctrl_type != '' else 'None',
        'Is_Control': is_control,
        'Gene_Symbol': gene_symbol if gene_symbol != '' else 'Unmapped',
        'Gene_Description': gpr_desc if gpr_desc != '' else cs_name,
        'CompositeSequence_ID': cs_id,
        'CompositeSequence_Name': cs_name,
        'Entrez_ID': entrez_id if entrez_id != '' else 'NA',
        'GC_Content': gc
    })

annot_df = pd.DataFrame(annot_records)
print("\n--- Annotation Summary ---")
print("Total Probes:", len(annot_df))
ctrl_probes = annot_df[annot_df['Is_Control'] == True]
exp_probes = annot_df[annot_df['Is_Control'] == False]
print(f"Control Probes: {len(ctrl_probes):,}")
print(f"Experimental Probes: {len(exp_probes):,}")

mapped_exp = exp_probes[exp_probes['Gene_Symbol'] != 'Unmapped']
unmapped_exp = exp_probes[exp_probes['Gene_Symbol'] == 'Unmapped']
print(f"Experimental Mapped to Gene Symbol: {len(mapped_exp):,} probes ({len(mapped_exp)/len(exp_probes)*100:.2f}%)")
print(f"Experimental Unmapped: {len(unmapped_exp):,} probes ({len(unmapped_exp)/len(exp_probes)*100:.2f}%)")

unique_genes = mapped_exp['Gene_Symbol'].nunique()
print(f"Unique Gene Symbols represented: {unique_genes:,}")

# Check duplicate probes per gene
gene_counts = mapped_exp['Gene_Symbol'].value_counts()
multi_probe_genes = gene_counts[gene_counts > 1]
print(f"Genes with multiple probes: {len(multi_probe_genes):,}")
print("Top 5 genes with most probes in experimental set:")
print(multi_probe_genes.head(5))

# Save Probe_Annotation.csv in both required locations
annot_csv1 = os.path.join(BASE_DIR, r"qc_annotation_outputs\tables\Probe_Annotation.csv")
annot_csv2 = os.path.join(BASE_DIR, r"Probe_Annotation.csv")
annot_df.to_csv(annot_csv1, index=False)
annot_df.to_csv(annot_csv2, index=False)
print(f"\nSaved Probe Annotation table to:\n - {annot_csv1}\n - {annot_csv2}")