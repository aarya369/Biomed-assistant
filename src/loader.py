import fitz
import hashlib
import json
import os

DATA_DIR = "data/papers"
OUTPUT_FILE = "outputs/documents.json"

def process_pdf(pdf_path):
    """Extract metadata and text from a single PDF."""

    with open(pdf_path, "rb") as f:
        document_id = hashlib.md5(f.read()).hexdigest()

    doc = fitz.open(pdf_path)
    metadata = doc.metadata

    pages = []

    for page_num in range(len(doc)):
        pages.append({
            "page_number": page_num + 1,
            "text": doc[page_num].get_text()
        })

    return {
        "document_id": document_id,
        "document_title": metadata.get("title") or os.path.basename(pdf_path),
        "authors": metadata.get("author") or "",
        "source_url": "unknown",
        "year": "",
        "pages": pages
    }

def build_documents():

    documents = []

    for filename in os.listdir(DATA_DIR):

        if not filename.endswith(".pdf"):
            continue

        pdf_path = os.path.join(DATA_DIR, filename)
        documents.append(process_pdf(pdf_path))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            documents,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Processed {len(documents)} documents")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    build_documents()
