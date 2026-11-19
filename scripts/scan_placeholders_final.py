import os
import re

repo_dir = r"C:\Users\ACER\BIoinformatics_Training\temp_audit_extraction\Gastric_Cancer_Bioinformatics_GSE17154"
patterns = [
    r"YOUR_USERNAME",
    r"your_username",
    r"example\.com",
    r"your-username",
    r"github\.com/example",
    r"your_email",
    r"\[insert",
    r"\[your",
    r"TODO",
    r"FIXME"
]

matches = []
for root, dirs, files in os.walk(repo_dir):
    for f in files:
        if f.endswith(('.md', '.py', '.cff', '.txt', '.yml', '.yaml', '.sh', '.bat', '.bib', '.json')):
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

print(f"Total placeholder matches: {len(matches)}")
for m in matches:
    print(m)
