import json, os, hashlib
INPUT_FILE = "outputs/recursive_chunks.json"
OUTPUT_FILE = "outputs/recursive_chunks_with_hash.json"

with open(INPUT_FILE, "r", encoding = "utf-8") as f:
    chunks = json.load(f)
all_chunks = []
for chunk in chunks:
    source_text = chunk["source_text"]
    hashed_text = hashlib.md5(source_text.encode("utf-8")).hexdigest()
    new_chunk = {
    "document_id": chunk["document_id"],
    "page_number": chunk["page_number"],
    "chunk_index": chunk["chunk_index"],
    "source_text": source_text,
    "content_hash": hashed_text
}
    all_chunks.append(new_chunk)
with open(OUTPUT_FILE, "w", encoding = "utf-8") as f:
    json.dump(all_chunks, f, indent = 2, ensure_ascii = False)
print(f"Chunks with hashes: {len(all_chunks)}")
    

