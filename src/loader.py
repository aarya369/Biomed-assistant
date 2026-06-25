import fitz
import hashlib
import json
import os

DATA_DIR = "data/papers"
OUTPUT_FILE = "outputs/documents.json"

documents = []

for filename in os.listdir(DATA_DIR):

    if not filename.endswith(".pdf"):
        continue

    pdf_path = os.path.join(DATA_DIR, filename)

    # document_id
    with open(pdf_path, "rb") as f:
        document_id = hashlib.md5(f.read()).hexdigest()

    # open pdf
    doc = fitz.open(pdf_path)

    metadata = doc.metadata

    title = metadata.get("title") or filename
    authors = metadata.get("author") or ""
    source_url = "unknown"
    year = ""

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

    documents.append(document)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(
        documents,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Processed {len(documents)} documents")
print(f"Saved to {OUTPUT_FILE}")