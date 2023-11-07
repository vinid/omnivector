from omnivector import PineconeDB, WeaviateDB, LanceDB

from omnivector.embedders import SentenceTransformerEmbedder
db = WeaviateDB()

encoder = SentenceTransformerEmbedder("paraphrase-MiniLM-L6-v2", device="cpu")


db.create_index()

print("First search")
docs = ["the cat is on the table", "the table is on the cat", "the dog is mining bitcoins"]
ids = list(range(4, len(docs) + 4))
embeddings = encoder.embed(docs)

db.add(ids, embeddings, [{"text": d} for d in docs])
search_vector = encoder.embed(["the dog is mining bitcoins"])[0]
print(db.vector_search(search_vector, k=1))

print()
print("Second search")

docs = ["the enemy of my enemy is my cousin"]
ids = [99]
embeddings = encoder.embed(docs)

db.add(ids, embeddings, [{"text": d} for d in docs])
search_vector = encoder.embed(["the enemy of my enemy is my cousin"])[0]
print(db.vector_search(search_vector, k=1))


