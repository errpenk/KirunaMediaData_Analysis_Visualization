
from sentence_transformers import SentenceTransformer, util

#Calculate semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

s1 = "How do I learn Python?"
s2 = "What's the best way to study Python?"
s3 = "I like eating pizza"

emb = model.encode([s1, s2, s3])

print(util.cos_sim(emb[0], emb[1]))  # High similarity ~0.85
print(util.cos_sim(emb[0], emb[2]))  # Low similarity ~0.08
