from omnivector.abstraction import  AbstractDB

class WeaviateDB(AbstractDB):

    def __init__(self):
        super().__init__()

        import weaviate
        import json

        self.client = weaviate.Client(
            url=self.config["weaviate"]["URL"],  # Replace with your endpoint
            auth_client_secret=weaviate.AuthApiKey(api_key=self.config["weaviate"]["API_KEY"]),
            # Replace w/ your Weaviate instance API key

        )

    def create_index(self, ids, text, vectors):
        class_obj = {
            "class": self.config["weaviate"]["CLASS"],
            "vectorizer": "none",
            # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        }

        self.client.schema.create_class(class_obj)

        self.client.batch.configure(batch_size=100)  # Configure batch
        with self.client.batch as batch:  # Configure a batch process
            for id, t, v in zip(ids,text,vectors):  # Batch import all Questions
                properties = {
                    "index": id,
                    "text": t,
                }
                batch.add_data_object(
                    data_object=properties,
                    class_name=self.config["weaviate"]["CLASS"],
                    vector=v  # Add custom vector
                )

    def vector_search(self, vector, k=3):
        import json
        response = (
            self.client.query
            .get(self.config["weaviate"]["CLASS"], ["index", "text"])
            .with_near_vector({
                "vector": vector
            })
            .with_limit(k)
            .with_additional(["distance"])
            .do()
        )

        return json.dumps(response, indent=4)
