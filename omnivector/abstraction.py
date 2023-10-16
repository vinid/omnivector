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






