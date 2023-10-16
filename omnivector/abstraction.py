import pandas as pd
import os
import pinecone
import time


class AbstractDB:

    def __init__(self):
        import yaml
        self.config = yaml.safe_load(open(os.environ["OMNIVECTOR_CONFIG"]))

    def create_index(self, ids, text, vectors):
        pass

    def vector_search(self, vector, k=1):
        pass


import random
import itertools

def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


class PineconeDB(AbstractDB):

    def __init__(self,):
        super().__init__()
        pinecone.init(
            api_key=self.config["pinecone"]['PINECONE_API_KEY'],
            environment=self.config["pinecone"]['GPC_ENVIRONMENT']
        )
        self.index_name = self.config["pinecone"]['INDEX_NAME']

    def create_index(self, ids, texts, vectors):
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


class LanceDB(AbstractDB):
    """
    LanceDB is a vector database that uses Lance to store and search vectors.
    """
    def __init__(self):
        super().__init__()

    def create_index(self, ids, texts, vectors):
        import lance
        import pyarrow as pa
        from lance.vector import vec_to_table

        data = pd.DataFrame({"text": texts, "id": ids})
        table = vec_to_table(vectors)

        combined = pa.Table.from_pandas(data).append_column("vector", table["vector"])
        ds = lance.write_dataset(combined, self.config["lancedb"]["DB_PATH"], mode="overwrite")


    def vector_search(self, vector, k=3):
        import lance
        self.ds = lance.dataset(self.config["lancedb"]["DB_PATH"])
        return self.ds.to_table(
            nearest={
                "column": "vector",
                "k": k,
                "q": vector,
                "nprobes": 20,
                "refine_factor": 100
            }).to_pandas()




class PGVectorDB(AbstractDB):
    def __init__(self):
        from pgvector.psycopg import register_vector
        import psycopg

        super().__init__()

        self.conn = psycopg.connect("dbname=template1 user=postgres password=your_password", autocommit=True)

        self.conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
        register_vector(self.conn)

    def create_index(self, ids, texts, vectors):
        self.conn.execute('DROP TABLE IF EXISTS documents')
        self.conn.execute('CREATE TABLE documents (id bigserial PRIMARY KEY, content text, embedding vector(384))')


        for id, content, embedding in zip(ids, texts, vectors):
            self.conn.execute('INSERT INTO documents (id, content, embedding) VALUES (%s, %s, %s)', (id, content, embedding))


    def vector_search(self, vector, k=3):
        neighbors = self.conn.execute('SELECT id, content FROM documents ORDER BY embedding <=> %s LIMIT 5', (vector,))

        return [n for n in  neighbors]


