from sentence_transformers import SentenceTransformer
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
import json, os
INPUT_FILE = "outputs/recursive_chunks_with_hash.json"
OUTPUT_FILE = "outputs/chunks_with_embeddings.json"
with open(INPUT_FILE, "r", encoding = "utf-8") as f:
    chunks = json.load(f)
old_hash_to_embedding = {}
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding = "utf-8") as f:
        old_chunks = json.load(f)
    for chunk in old_chunks:
        if("content_hash" in chunk and "embedding" in chunk):
            old_hash_to_embedding[chunk["content_hash"]] = chunk["embedding"]
reused = 0
new = 0
for chunk in chunks:
    content_hash = chunk["content_hash"]
    if content_hash in old_hash_to_embedding:
        chunk["embedding"] = old_hash_to_embedding[content_hash]
        reused += 1
    else:
        chunk["embedding"] = model.encode(chunk["source_text"]).tolist()
        new += 1
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(
        chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Total Chunks: {len(chunks)}")
print(f"Reused embeddings: {reused}")
print(f"New embeddings: {new}")

if len(chunks) > 0:
    print(
        f"Embedding Dimension: "
        f"{len(chunks[0]['embedding'])}"
    )

# all_chunks = []
# for chunk in chunks:
#     embedding = model.encode(chunk["source_text"])
#     listed_embedding = embedding.tolist()
#     new_chunk = {
#     "document_id": chunk["document_id"],
#     "page_number": chunk["page_number"],
#     "chunk_index": chunk["chunk_index"],
#     "source_text": chunk["source_text"],
#     "content_hash": chunk["content_hash"],
#     "embedding": listed_embedding
# }
#     all_chunks.append(new_chunk)
# with open(OUTPUT_FILE, "w", encoding = "utf-8") as f:
#     json.dump(all_chunks, f, indent = 2, ensure_ascii = False)
