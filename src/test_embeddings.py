import json
import numpy as np

# Load chunks
with open("outputs/chunks_with_embeddings.json", "r") as f:
    chunks = json.load(f)

# Convert embeddings to numpy array
embeddings = np.array([chunk["embedding"] for chunk in chunks])


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Pick any three chunks
import random

test_indices = random.sample(range(len(chunks)), 3)

for idx in test_indices:

    print("=" * 80)
    print(f"QUERY CHUNK {idx}\n")

    print(chunks[idx]["source_text"][:500])
    print("\n")

    similarities = []

    for i in range(len(chunks)):

        if i == idx:
            continue

        sim = cosine_similarity(
            embeddings[idx],
            embeddings[i]
        )

        similarities.append((i, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)

    print("Top 5 nearest neighbours:\n")

    for rank, (i, sim) in enumerate(similarities[:5], start=1):

        print(f"{rank}. Chunk {i}   Similarity = {sim:.4f}")
        print(chunks[i]["source_text"][:300])
        print("-" * 60)