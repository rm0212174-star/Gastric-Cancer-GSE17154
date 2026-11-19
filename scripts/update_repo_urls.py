import os

files = [
    r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis\CITATION.cff",
    r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis\README.md",
    r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis\FINAL_GITHUB_README.md",
    r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis\FINAL_REPRODUCIBILITY_GUIDE.md",
    r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis\REPRODUCIBILITY.md",
    r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis\docs\REPRODUCIBILITY.md",
    r"C:\Users\ACER\Bioinformatics_Training\12_Real_GSE17154_Analysis\reports\REPRODUCIBILITY.md"
]

for f in files:
    if os.path.exists(f):
        with open(f, "r", encoding="utf-8") as fh:
            c = fh.read()
        c = c.replace("Rahul-Bioinformatics/Gastric-Cancer-GSE17154", "rm0212174-star/Gastric-Cancer-GSE17154")
        c = c.replace("cd gastric-cancer-gse17154", "cd Gastric-Cancer-GSE17154")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(c)

print("Updated URLs successfully to rm0212174-star/Gastric-Cancer-GSE17154.")
