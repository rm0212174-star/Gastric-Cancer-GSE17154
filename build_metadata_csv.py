import gzip
import csv
import pandas as pd

series_matrix_path = r"12_Real_GSE17154_Analysis\raw_downloads\GSE17154_series_matrix.txt.gz"

headers = {}
in_header = True

with gzip.open(series_matrix_path, 'rt', encoding='utf-8', errors='replace') as f:
    for line in f:
        line_clean = line.rstrip('\r\n')
        if line_clean.startswith('!series_matrix_table_begin'):
            break
        if line_clean.startswith('!Sample_'):
            parts = line_clean.split('\t')
            key = parts[0]
            vals = [p.strip('"') for p in parts[1:]]
            if key not in headers:
                headers[key] = vals
            else:
                # If repeated key (e.g. characteristics_ch1), append or collect
                if isinstance(headers[key][0], list):
                    headers[key].append(vals)
                else:
                    headers[key] = [headers[key], vals]

print(f"Sample keys found: {list(headers.keys())}")
n_samples = len(headers['!Sample_geo_accession'])
print(f"Sample count: {n_samples}")

records = []
for i in range(n_samples):
    gsm = headers['!Sample_geo_accession'][i]
    title = headers['!Sample_title'][i]
    
    # Characteristics might be list of lists if multiple lines
    chars = headers.get('!Sample_characteristics_ch1', [])
    char_vals = []
    if isinstance(chars[0], list):
        char_vals = [line[i] for line in chars if i < len(line)]
    else:
        char_vals = [chars[i]]
        
    source = headers.get('!Sample_source_name_ch1', [''])[i]
    organism = headers.get('!Sample_organism_ch1', [''])[i]
    ch1 = headers.get('!Sample_label_ch1', [''])[i]
    ch2 = headers.get('!Sample_label_ch2', [''])[i]
    platform = headers.get('!Sample_platform_id', [''])[i]
    
    # Classify group based on Title
    if title.startswith('CANCER'):
        grp = 'CANCER'
    elif title.startswith('PN'):
        grp = 'Paired_Normal_PN'
    elif title.startswith('AN'):
        grp = 'Apparently_Normal_AN'
    else:
        grp = 'UNKNOWN'
        
    records.append({
        'GEO_Accession': gsm,
        'Title': title,
        'Sample_Group': grp,
        'Source_Name_ch1': source,
        'Organism': organism,
        'Channel_1_Cy5': ch1,
        'Channel_2_Cy3': ch2,
        'Platform_ID': platform,
        'Characteristics': " | ".join(char_vals)
    })

df = pd.DataFrame(records)
print(df.head())
print("\nGroup counts:")
print(df['Sample_Group'].value_counts())

csv_out = r"12_Real_GSE17154_Analysis\metadata\GSE17154_real_sample_metadata.csv"
df.to_csv(csv_out, index=False)
print(f"\nSaved metadata CSV to: {csv_out}")
