import os

def scan_pdfs(base_path):
    pdfs = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, file))
    return pdfs
