import time
from omnivector import PineconeDB, WeaviateDB, LanceDB
from omnivector.embedders import SentenceTransformerEmbedder
db = LanceDB()
sleep = 1

encoder = SentenceTransformerEmbedder("paraphrase-MiniLM-L6-v2", device="cpu")
db.create_index()
# sleep to allow indexing to finish
time.sleep(sleep)

#######################
# We add first set of vectors
#######################

print("First search")
docs = ["the cat is on the table", "the table is on the cat", "the dog is mining bitcoins"]
ids = list(range(4, len(docs) + 4))
embeddings = encoder.embed(docs)

db.add(ids, embeddings, [{"text": d} for d in docs])

# sleep to allow indexing to finish
time.sleep(sleep)

#######################
# We search for a vector
#######################
search_vector = encoder.embed(["the dog is mining bitcoins"])[0]
print(db.vector_search(search_vector, k=1))


#######################
# New addition
#######################

docs = ["the enemy of my enemy is my cousin"]
ids = [99]
embeddings = encoder.embed(docs)

db.add(ids, embeddings, [{"text": d} for d in docs])

# sleep to allow indexing to finish
time.sleep(sleep)

print()
print("Second search")

#######################
# We search for a vector
#######################
search_vector = encoder.embed(["the enemy of my enemy is my cousin"])[0]
print(db.vector_search(search_vector, k=1))


#######################
# We delete the vector
#######################

db.delete([99])

# sleep to allow indexing to finish
time.sleep(sleep)

print()
print("Third search")


#######################
# We search for a vector
#######################

search_vector = encoder.embed(["the enemy of my enemy is my cousin"])[0]
print(db.vector_search(search_vector, k=1))
