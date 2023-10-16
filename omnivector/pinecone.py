import itertools
from omnivector.abstraction import AbstractDB
import time

def chunks(iterable, batch_size=100):
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


class PineconeDB(AbstractDB):
    def __init__(self,):
        super().__init__()
        import pinecone
        pinecone.init(
            api_key=self.config["pinecone"]['PINECONE_API_KEY'],
            environment=self.config["pinecone"]['GPC_ENVIRONMENT']
        )
        self.index_name = self.config["pinecone"]['INDEX_NAME']

    def create_index(self, ids, texts, vectors):
        import pinecone
        # only create index if it doesn't exist
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.index_name,
                dimension=len(vectors[0]),
                metric='cosine'
            )
            # wait a moment for the index to be fully initialized
            time.sleep(1)

        # now connect to the index
        self.index = pinecone.GRPCIndex(self.index_name)

        all_data = []

        for idx, txt, emb in zip(ids, texts, vectors):
            all_data.append({
                 "id": f"vec_{idx}",
                 "values": emb.tolist(),
                 'metadata': {'text': txt}})

        for ids_vectors_chunk in chunks(all_data, batch_size=100):
            print(ids_vectors_chunk[0])
            self.index.upsert(vectors=list(ids_vectors_chunk))

    def vector_search(self, vector, k=1):
        # now query
        xc = self.index.query(vector.tolist(), top_k=k, include_metadata=True)
        return xc







