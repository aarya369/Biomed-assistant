import json
import os
INPUT_FILE = "outputs/documents.json"
OUTPUT_FILE = "outputs/fixed_chunks.json"
CHUNK_SIZE = 1000
OVERLAP = 100
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)
all_chunks = []
for document in documents:
    document_id = document["document_id"]
    for page in document["pages"]:
        page_number = page["page_number"]
        text = page["text"]
        start = 0
        chunk_index = 0
        while start< len(text):
            end = start + CHUNK_SIZE
            chunk_text = text[start:end]
            chunk = {
                "document_id": document_id,
                "page_number": page_number,
                "chunk_index": chunk_index,
                "source_text": chunk_text
            }
            all_chunks.append(chunk)
            chunk_index += 1
            start = start + CHUNK_SIZE - OVERLAP

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(
        all_chunks,
        f,
        indent=2,
        ensure_ascii=False
    )
print(f"Total Chunks: {len(all_chunks)}")
print(f"Saved to: {OUTPUT_FILE}")