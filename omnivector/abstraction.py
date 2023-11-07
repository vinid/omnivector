import os

class AbstractDB:

    def __init__(self):
        import yaml
        self.config = yaml.safe_load(open(os.environ["OMNIVECTOR_CONFIG"]))

    def create_index(self):
        pass

    def add(self, ids, vectors, metadata=None):
        pass

    def vector_search(self, vector, k=1):
        pass






