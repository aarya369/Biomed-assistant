from retriever import retrieve_chunks

chunks = retrieve_chunks(
    "Which universities were involved in the study Modulation of motor cortex excitability in obsessive-compulsive disorder?"
)

for i, chunk in enumerate(chunks):

    print("=" * 80)
    print(f"Chunk {i+1}")
    print(chunk["metadata"])
    print()
    print(chunk["text"][:700])