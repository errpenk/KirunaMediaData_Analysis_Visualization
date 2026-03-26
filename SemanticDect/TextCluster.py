# K-Means clustering on sentence embeddings

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

model = SentenceTransformer("all-MiniLM-L6-v2")

# text
sentences = [
    "Kiruna is being relocated due to mining subsidence.",
    "LKAB iron ore mine expands beneath the city.",
    "The Sami people have herded reindeer here for centuries.",
    "The new Kiruna city centre opens in 2024.",
    "Ice Hotel attracts thousands of tourists every winter.",
    "Northern lights are visible from October to March.",
    "The church was moved brick by brick to its new site.",
    "Rare earth minerals discovered in northern Sweden.",
]


N_CLUSTERS = 3   # change

embeddings = model.encode(sentences)

kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=0, n_init="auto")
labels = kmeans.fit_predict(embeddings)

print(f"Clustered {len(sentences)} sentences into {N_CLUSTERS} groups:\n")
for label, sent in sorted(zip(labels, sentences)):
    print(f"  Cluster {label}: {sent}")
