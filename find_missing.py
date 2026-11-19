import gzip

path = r"12_Real_GSE17154_Analysis\raw_downloads\GSE17154_series_matrix.txt.gz"
with gzip.open(path, 'rt', encoding='utf-8') as f:
    for line in f:
        if line.startswith('!series_matrix_table_begin'):
            header = f.readline().strip().split('\t')
            samples = [s.strip('"') for s in header[1:]]
            row_idx = 0
            for line in f:
                if line.startswith('!series_matrix_table_end'):
                    break
                row_idx += 1
                parts = line.strip().split('\t')
                probe_id = parts[0].strip('"')
                for col_idx, val in enumerate(parts[1:]):
                    val_clean = val.strip('"').strip()
                    if val_clean == '' or val_clean == 'null' or val_clean == 'NA' or val_clean == 'NaN':
                        print(f"Missing value found! Row={row_idx}, Probe_ID={probe_id}, Sample={samples[col_idx]}, Value={repr(val)}")
            break
