import os
import re

extract_dir = r"C:\Users\ACER\BIoinformatics_Training\temp_audit_extraction\Gastric_Cancer_Bioinformatics_GSE17154"

patterns = {
    "placeholder_url": re.compile(r"https?://(?:www\.)?github\.com/example/[^\s\)\"\'>]+"),
    "dummy_text": re.compile(r"\b(dummy|placeholder|your_username|TODO|FIXME)\b", re.IGNORECASE),
    "secrets": re.compile(r"\b(api[_-]?key|secret[_-]?key|password)\b\s*[:=]\s*[\'\"][^\'\"]+[\'\"]", re.IGNORECASE)
}

findings = []

for root, dirs, files in os.walk(extract_dir):
    for f in files:
        if f.endswith(('.png', '.gz', '.tar', '.zip', '.pyc')):
            continue
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, extract_dir)
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                for line_no, line in enumerate(fh, 1):
                    for p_name, pat in patterns.items():
                        m = pat.search(line)
                        if m:
                            findings.append((rel, line_no, p_name, m.group(0), line.strip()[:100]))
        except Exception as e:
            print("Error reading", rel, e)

print(f"Total findings: {len(findings)}")
for rel, line_no, p_name, matched, line in findings:
    print(f"[{p_name}] {rel}:{line_no} -> {matched} (Context: {line})")
