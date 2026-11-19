import os
import re

repo_dir = r"C:\Users\ACER\BIoinformatics_Training\temp_audit_extraction\Gastric_Cancer_Bioinformatics_GSE17154"
patterns = [
    r"ghp_[A-Za-z0-9_]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"AIza[0-9A-Za-z-_]{35}",
    r"bearer\s+[A-Za-z0-9\-\._~\+\/]+=*",
    r"password\s*[:=]\s*['\"][^'\"]+['\"]",
    r"secret\s*[:=]\s*['\"][^'\"]+['\"]"
]

matches = []
for root, dirs, files in os.walk(repo_dir):
    for f in files:
        if f.endswith(('.md', '.py', '.cff', '.txt', '.yml', '.yaml', '.sh', '.bat', '.bib', '.json', '.csv')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                    lines = fh.readlines()
                    for idx, line in enumerate(lines):
                        for pat in patterns:
                            if re.search(pat, line, re.IGNORECASE):
                                matches.append((os.path.relpath(p, repo_dir), idx+1, pat, line.strip()[:100]))
            except Exception as e:
                pass

print(f"Total sensitive token matches: {len(matches)}")
for m in matches:
    print(m)
