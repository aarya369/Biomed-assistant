from sentence_transformers import SentenceTransformer
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
text = "This is a test sentence"
embedding = model.encode(text)
print(type(embedding))
print(embedding.shape)
