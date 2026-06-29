import json
import chromadb

def build_vector():
    #Store everything permanently inside the folder data/chroma_db
    client = chromadb.PersistentClient("data/chroma_db")
    try:
        client.delete_collection("biomedical_chunks")  # optional
    except Exception:
        pass
    collection = client.get_or_create_collection("biomedical_chunks", metadata={"hnsw:space": "cosine"})


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
            "chunk_index" : chunk["chunk_index"],
            "title": chunk["document_title"]

        }]
    )
    if __name__ == '__main__':
        build_vector()
