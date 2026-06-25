import json
import chromadb
from chromadb.config import Settings

#Store everything permanently inside the folder data/chroma_db
client = chromadb.PersistentClient("data/chroma_db")

collection = client.get_or_create_collection(
    name = "biomedical_chunks"
)
with open("outputs/chunks_with_embeddings.json", "r", encoding = "utf-8") as f:
    chunks = json.load(f)
for chunk in chunks:
    collection.add(
        ids = [chunk["content_hash"]],
        embeddings = [chunk["embedding"]],
        documents = [chunk["source_text"]],
        metadatas = [{
            "document_id" : chunk["document_id"],
            "page_number" : chunk["page_number"],
            "chunk_index" : chunk["chunk_index"]

        }]

    )
print(f"Total chunks stored: {collection.count()}")
