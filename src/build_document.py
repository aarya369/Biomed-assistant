import fitz
import hashlib

pdf_path = "../data/papers/000351346.pdf"

# Document ID
with open(pdf_path, "rb") as f:
    document_id = hashlib.md5(f.read()).hexdigest()

# Open PDF
doc = fitz.open(pdf_path)

# Metadata
metadata = doc.metadata

title = metadata.get("title") or pdf_path.split("/")[-1]
authors = metadata.get("author") or ""
source_url = "unknown"
year = ""

# Pages
pages = []

for page_num in range(len(doc)):

    pages.append(
        {
            "page_number": page_num + 1,
            "text": doc[page_num].get_text()
        }
    )

document = {
    "document_id": document_id,
    "title": title,
    "authors": authors,
    "source_url": source_url,
    "year": year,
    "pages": pages
}

print(document.keys())
print(document["document_id"])
print(document["title"])
print(len(document["pages"]))