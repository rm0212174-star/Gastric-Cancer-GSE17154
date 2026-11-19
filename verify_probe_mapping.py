import gzip
import csv

series_matrix_path = r"12_Real_GSE17154_Analysis\raw_downloads\GSE17154_series_matrix.txt.gz"
soft_path = r"12_Real_GSE17154_Analysis\raw_downloads\GPL6699_family.soft.gz"

print("Reading Series Matrix probe IDs...")
sm_probes = []
with gzip.open(series_matrix_path, 'rt', encoding='utf-8', errors='replace') as f:
    in_table = False
    for line in f:
        line_clean = line.rstrip('\r\n')
        if not in_table:
            if line_clean.startswith('!series_matrix_table_begin'):
                in_table = True
        else:
            if line_clean.startswith('!series_matrix_table_end'):
                break
            parts = line_clean.split('\t')
            probe_id = parts[0].strip('"')
            if probe_id != 'ID_REF':
                sm_probes.append(probe_id)

print(f"Total probes in series matrix: {len(sm_probes):,}")
print(f"Sample probe IDs (first 5): {sm_probes[:5]}")

print("\nReading GPL6699 probe IDs...")
soft_probes = set()
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
                id_col = header.index('ID')
            else:
                parts = line_clean.split('\t')
                soft_probes.add(parts[id_col])

print(f"Total probes in GPL6699 soft: {len(soft_probes):,}")

# Check matching
sm_set = set(sm_probes)
matched = sm_set.intersection(soft_probes)
print(f"Direct ID matches: {len(matched):,} / {len(sm_set):,} ({len(matched)/len(sm_set)*100:.2f}%)")

if len(matched) < len(sm_set):
    missing = list(sm_set - soft_probes)[:5]
    print(f"Example missing in GPL: {missing}")
    example_gpl = list(soft_probes)[:5]
    print(f"Example GPL IDs: {example_gpl}")
