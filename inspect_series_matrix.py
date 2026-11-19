"""
inspect_series_matrix.py
Validates the official GSE17154_series_matrix.txt.gz:
- Counts samples and probes
- Parses headers and characteristics
- Checks value distributions, missing values, and data scale
"""

import gzip
import os
import hashlib
import numpy as np
import pandas as pd

MATRIX_PATH = r"12_Real_GSE17154_Analysis\raw_downloads\GSE17154_series_matrix.txt.gz"

def get_file_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192 * 1024):
            sha.update(chunk)
    return sha.hexdigest()

def inspect_matrix():
    print("=" * 80)
    print("INSPECTING GSE17154 SERIES MATRIX")
    print("=" * 80)
    
    sz = os.path.getsize(MATRIX_PATH)
    sha = get_file_sha256(MATRIX_PATH)
    print(f"File Size: {sz:,} bytes ({sz / (1024*1024):.2f} MB)")
    print(f"SHA-256 Checksum: {sha}")
    
    metadata = {}
    char_lines = []
    data_lines = []
    in_table = False
    
    with gzip.open(MATRIX_PATH, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line_str = line.strip()
            if not in_table:
                if line_str.startswith('!Sample_title'):
                    metadata['Title'] = [p.strip().strip('"') for p in line_str.split('\t')[1:]]
                elif line_str.startswith('!Sample_geo_accession'):
                    metadata['GEO_Accession'] = [p.strip().strip('"') for p in line_str.split('\t')[1:]]
                elif line_str.startswith('!Sample_source_name_ch1'):
                    metadata['Source_ch1'] = [p.strip().strip('"') for p in line_str.split('\t')[1:]]
                elif line_str.startswith('!Sample_source_name_ch2'):
                    metadata['Source_ch2'] = [p.strip().strip('"') for p in line_str.split('\t')[1:]]
                elif line_str.startswith('!Sample_characteristics_ch1'):
                    char_lines.append([p.strip().strip('"') for p in line_str.split('\t')[1:]])
                elif line_str.startswith('!Sample_label_ch1'):
                    metadata['Label_ch1'] = [p.strip().strip('"') for p in line_str.split('\t')[1:]]
                elif line_str.startswith('!Sample_label_ch2'):
                    metadata['Label_ch2'] = [p.strip().strip('"') for p in line_str.split('\t')[1:]]
                elif line_str.startswith('!Sample_description'):
                    metadata['Description'] = [p.strip().strip('"') for p in line_str.split('\t')[1:]]
                elif line_str.startswith('!Sample_data_processing'):
                    metadata['Data_Processing'] = [p.strip().strip('"') for p in line_str.split('\t')[1:]]
                elif line_str.startswith('!series_matrix_table_begin'):
                    in_table = True
            else:
                if line_str.startswith('!series_matrix_table_end'):
                    break
                data_lines.append(line_str)
                
    print(f"\nMetadata extracted:")
    print(f"  Number of Samples: {len(metadata.get('GEO_Accession', []))}")
    print(f"  Data Processing Statement (first sample):")
    if 'Data_Processing' in metadata and metadata['Data_Processing']:
        print(f"    \"{metadata['Data_Processing'][0]}\"")
        
    print(f"\nCharacteristics lines count: {len(char_lines)}")
    for idx, ch in enumerate(char_lines):
        unique_tags = set(c.split(':')[0] if ':' in c else c for c in ch if c)
        print(f"  Line {idx+1}: {unique_tags}")
        
    # Analyze table headers and probe count
    header = data_lines[0].split('\t')
    col_names = [p.strip().strip('"') for p in header]
    print(f"\nMatrix Table Header:")
    print(f"  Probe ID column: {col_names[0]}")
    print(f"  Sample columns: {len(col_names) - 1} samples")
    print(f"  Total Data Rows (Probes): {len(data_lines) - 1:,}")
    
    # Read matrix into dataframe for numerical inspection
    from io import StringIO
    print("\nParsing expression values for numerical distribution...")
    table_str = "\n".join(data_lines)
    df_expr = pd.read_csv(StringIO(table_str), sep='\t', index_col=0)
    print(f"DataFrame Shape: {df_expr.shape[0]:,} probes x {df_expr.shape[1]} samples")
    
    # Check nulls and range
    null_counts = df_expr.isna().sum().sum()
    total_elements = df_expr.size
    print(f"Missing Values: {null_counts:,} / {total_elements:,} ({null_counts / total_elements * 100:.2f}%)")
    
    # Value range
    flat_vals = df_expr.values.flatten()
    valid_vals = flat_vals[~np.isnan(flat_vals)]
    print(f"Value Distribution:")
    print(f"  Min: {np.min(valid_vals):.4f}")
    print(f"  25th Percentile: {np.percentile(valid_vals, 25):.4f}")
    print(f"  Median: {np.median(valid_vals):.4f}")
    print(f"  Mean: {np.mean(valid_vals):.4f}")
    print(f"  75th Percentile: {np.percentile(valid_vals, 75):.4f}")
    print(f"  Max: {np.max(valid_vals):.4f}")
    print(f"  Std: {np.std(valid_vals):.4f}")
    
    # Check sample titles and groups
    titles = metadata['Title']
    cancer = [t for t in titles if 'CANCER' in t]
    pn = [t for t in titles if 'PN -' in t]
    an = [t for t in titles if 'AN -' in t]
    print(f"\nSample Group Breakdown:")
    print(f"  CANCER: {len(cancer)} samples")
    print(f"  Paired Normal (PN): {len(pn)} samples")
    print(f"  Apparently Normal (AN): {len(an)} samples")
    print(f"  Total: {len(cancer) + len(pn) + len(an)} samples")
    
    # Check description fields for patient pairing
    print("\nInspecting Sample Description & Characteristics for Patient Pairing:")
    for i in range(len(titles)):
        desc = metadata.get('Description', [''])[i] if 'Description' in metadata else ''
        chars = [ch[i] for ch in char_lines]
        if i < 8 or i >= len(titles) - 4:
            print(f"  [{metadata['GEO_Accession'][i]}] {titles[i]} | Desc: '{desc}' | Chars: {chars}")

if __name__ == "__main__":
    inspect_matrix()
