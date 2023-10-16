from omnivector.abstraction import *
import os
from omnivector.embedders import SentenceTransformerEmbedder

db = LanceDB()

encoder = SentenceTransformerEmbedder("paraphrase-MiniLM-L6-v2", device="cpu")

docs = ["the cat is on the table", "the table is on the cat", "the dog is mining bitcoins"]

print(docs[0], len(docs))
# ids = ["1", "2"]*200
ids = list(range(1, len(docs) + 1))
embeddings = encoder.embed(docs)

db.create_index(ids, docs, embeddings)

search_vector = encoder.embed(["the dog is mining bitcoins"])[0]
print(db.vector_search(search_vector, k=1))


