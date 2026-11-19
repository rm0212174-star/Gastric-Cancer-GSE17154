"""
inspect_publication.py
Extracts exact text from PMC3004887 regarding samples, pairing, and microarray analysis.
"""

import xml.etree.ElementTree as ET
import re

tree = ET.parse(r"12_Real_GSE17154_Analysis\metadata\PMC3004887_publication.xml")
root = tree.getroot()

text = ' '.join(root.itertext())

queries = [
    'paired normal', 'apparently normal', 'brb-arraytools', 'normalization',
    'pairing', 'stratagene', '44k', 'agilent', 'microarray analysis'
]

print("\n=== SUPPLEMENTARY MATERIAL IN PUBLICATION ===")
for elem in root.iter():
    if elem.tag in ['supplementary-material', 'table-wrap']:
        caption = elem.find('.//caption')
        cap_text = ' '.join(caption.itertext()) if caption is not None else ''
        href = elem.attrib.get('{http://www.w3.org/1999/xlink}href', '')
        print(f"Tag: {elem.tag} | ID: {elem.attrib.get('id', '')} | Href: {href}")
        print(f"   Caption: {cap_text[:200]}")
