class AbstractEmbedder:
    def __init__(self, **kwargs):
       pass

class OpenAIEmbedder(AbstractEmbedder):

    def __init__(self):
        super().__init__()

    def embed(self, sentences):
        pass


class SentenceTransformerEmbedder(AbstractEmbedder):
    def __init__(self, model_path, device="cpu"):
        super().__init__()
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_path)
        self.model.to(device)

    def embed(self, sentences):
        return self.model.encode(sentences, show_progress_bar=True)

