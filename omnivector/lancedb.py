import pandas as pd
from omnivector.abstraction import AbstractDB

class LanceDB(AbstractDB):
    """
    LanceDB is a vector database that uses Lance to store and search vectors.
    """
    def __init__(self):
        super().__init__()

    def create_index(self, ids, vectors, metadata=None):
        import lance
        import pyarrow as pa
        from lance.vector import vec_to_table


        data = pd.DataFrame({"id": ids})

        if metadata is not None:
            meta_df = pd.DataFrame.from_records(metadata)
            data = pd.concat([data, meta_df], axis=1)
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
