import chromadb
from sentence_transformers import SentenceTransformer

# Load the same embedding model used during indexing
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2")

# Connect to the existing ChromaDB
client = chromadb.PersistentClient(path="data/chroma_db")

collection = client.get_collection("biomedical_chunks")

def retrieve_chunks(query, k = 5):
    # Convert the query into an embedding
    query_embedding = model.encode(query).tolist()

    # Retrieve the top 5 most similar chunks
    results = collection.query(
    query_embeddings=[query_embedding],
    n_results=k
)
    retrieved_chunks = []
    for i in range(len(results["ids"][0])):
        retrieved_chunks.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })
    return retrieved_chunks
