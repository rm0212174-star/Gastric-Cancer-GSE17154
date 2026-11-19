import urllib.request
import json
import os

target_path = r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis\LICENSE"
req = urllib.request.Request(
    "https://api.github.com/licenses/mit",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode("utf-8"))
    license_body = data["body"]

license_body = license_body.replace("[year]", "2026")
license_body = license_body.replace("[fullname]", "Rahul Mishra")

with open(target_path, "w", encoding="utf-8") as f:
    f.write(license_body)

print("Created LICENSE successfully.")
