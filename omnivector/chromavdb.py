from omnivector.abstraction import  AbstractDB
import chromadb
from chromadb.config import Settings



class ChromaVDB(AbstractDB):

    def __init__(self):
        super().__init__()
        self.client = chromadb.PersistentClient(path=self.config["chroma"]["DB_PATH"])

        self.collection = None

    def id_to_str(self, ids):
        return [str(f"vec_{i}") for i in ids]

    def create_index(self):
        self.collection = self.client.create_collection(name=self.config["chroma"]["INDEX_NAME"])

    def add(self, ids, vectors, metadata=None):
        self.collection.add(
            embeddings=vectors.tolist(),
            metadatas = metadata,
            ids = self.id_to_str(ids)
        )


    def delete(self, ids):
        self.collection.delete(ids=self.id_to_str(ids))

    def vector_search(self, vector, k=3):

        response = self.collection.query(query_embeddings=vector.tolist(), n_results=k)


        return response
