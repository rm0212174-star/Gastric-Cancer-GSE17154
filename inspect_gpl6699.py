import gzip
import os

soft_path = r"12_Real_GSE17154_Analysis\raw_downloads\GPL6699_family.soft.gz"
print(f"Checking GPL6699 SOFT file: {soft_path}")
print(f"File size: {os.path.getsize(soft_path):,} bytes")

header_lines = []
table_header = None
first_rows = []
total_rows = 0
in_table = False

with gzip.open(soft_path, 'rt', encoding='utf-8', errors='replace') as f:
    for line in f:
        line_clean = line.rstrip('\r\n')
        if not in_table:
            if line_clean.startswith('!platform_table_begin'):
                in_table = True
                continue
            elif line_clean.startswith('^PLATFORM') or line_clean.startswith('!Platform_'):
                header_lines.append(line_clean)
        else:
            if line_clean.startswith('!platform_table_end'):
                break
            if table_header is None:
                table_header = line_clean.split('\t')
            else:
                total_rows += 1
                if len(first_rows) < 5:
                    first_rows.append(line_clean.split('\t'))

print(f"\n--- Platform Header Meta (first 10) ---")
for h in header_lines[:10]:
    print(h)

print(f"\n--- Platform Table Columns ({len(table_header) if table_header else 0}) ---")
if table_header:
    print(table_header)

print(f"\nTotal probe entries in GPL6699 table: {total_rows:,}")
print(f"\n--- First 2 rows ---")
for r in first_rows[:2]:
    if table_header:
        sample_dict = dict(zip(table_header[:8], r[:8]))
        print(sample_dict)
