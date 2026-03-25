from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [KirunaTextList] 
embeddings = model.encode(sentences)

# Clustering
kmeans = KMeans(n_clusters=5, random_state=0)
labels = kmeans.fit_predict(embeddings)

for i, (sent, label) in enumerate(zip(sentences, labels)):
    print(f"cluster {label}: {sent}")
