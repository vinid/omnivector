import pandas as pd
from omnivector.abstraction import AbstractDB

class LanceDB(AbstractDB):
    """
    LanceDB is a vector database that uses Lance to store and search vectors.
    """
    def __init__(self):
        super().__init__()

    def create_index(self):
        # not sure how to do this in Lance
        pass

    def delete(self, ids):
        import lancedb
        db = lancedb.connect(self.config["lancedb"]["DB_PATH"])

        tbl = db.open_table("my_table")
        ids = ", ".join(str(v) for v in ids)

        tbl.delete(f"id IN ({ids})")

    def add(self, ids, vectors, metadata=None):
        import lancedb
        data = pd.DataFrame({"id": ids})

        db = lancedb.connect(self.config["lancedb"]["DB_PATH"])

        if metadata is not None:
            meta_df = pd.DataFrame.from_records(metadata)
            data = pd.concat([data, meta_df], axis=1)

        data["vector"] = vectors.tolist()


        try:
            tbl = db.open_table("my_table")
            tbl.add(data)
        except:
            db.create_table("my_table", data)


    def vector_search(self, vector, k=3):
        import lancedb
        db = lancedb.connect(self.config["lancedb"]["DB_PATH"])

        tbl = db.open_table("my_table")

        return tbl.search(vector).limit(k).to_df()


