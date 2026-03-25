from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight English model

sentences = [
    "I love machine learning",
    "Deep learning is amazing",
    "xxxxEXAMPLE",
]

embeddings = model.encode(sentences)
print(embeddings.shape) 
