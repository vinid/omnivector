from omnivector import PineconeDB, WeaviateDB, LanceDB, PGVectorDB

from omnivector.embedders import SentenceTransformerEmbedder
db = LanceDB()

encoder = SentenceTransformerEmbedder("paraphrase-MiniLM-L6-v2", device="cpu")
docs = ["the cat is on the table", "the table is on the cat", "the dog is mining bitcoins"]


ids = list(range(4, len(docs) + 4))
embeddings = encoder.embed(docs)

db.create_index(ids, embeddings, [{"text": d} for d in docs])

search_vector = encoder.embed(["the dog is mining bitcoins"])[0]
print(db.vector_search(search_vector, k=1))


