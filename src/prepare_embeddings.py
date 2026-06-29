import hashlib
import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

INPUT_FILE = "outputs/documents.json"
OUTPUT_FILE = "outputs/chunks_with_embeddings.json"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n","\n",". "," ",""]
)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def chunk_documents():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)
    chunks = []
    for document in documents:
        for page in document["pages"]:
            split_chunks = splitter.split_text(page["text"])
            for idx, text in enumerate(split_chunks):
                chunks.append({
                    "document_id": document["document_id"],
                    "document_title": document["document_title"],
                    "page_number": page["page_number"],
                    "chunk_index": idx,
                    "source_text": text,
                    "content_hash": hashlib.md5(text.encode("utf-8")).hexdigest()
                })
    return chunks
def reuse_old_embeddings():
    if not os.path.exists(OUTPUT_FILE):
        return {}
    with open(OUTPUT_FILE, "r", encoding = "utf-8") as f:
        old_chunks = json.load(f)
    hash_to_embedding = {}
    for chunk in old_chunks:
        if ("content_hash" in chunk and "embedding" in chunk):
            hash_to_embedding[chunk["content_hash"]] = chunk["embedding"]
    return hash_to_embedding


def generate_embeddings(chunks):
    old_embeddings = reuse_old_embeddings()
    reused = 0
    new = 0
    for chunk in chunks:
        if chunk["content_hash"] in old_embeddings:
            chunk["embedding"] = old_embeddings[chunk["content_hash"]]
            reused += 1
        else:
            chunk["embedding"] = model.encode(chunk["source_text"]).tolist()
            new += 1

    print(f"Total Chunks: {len(chunks)}")
    print(f"Reused embeddings: {reused}")
    print(f"New embeddings: {new}")
    return chunks

def main():
    chunks = chunk_documents()
    chunks = generate_embeddings(chunks)
    with open(OUTPUT_FILE,"w",encoding="utf-8") as f:
        json.dump(chunks,f,indent=2,ensure_ascii=False)

if __name__ == "__main__":
    main()