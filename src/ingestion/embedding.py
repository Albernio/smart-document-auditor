from sentence_transformers import SentenceTransformer

from src.models import Embedding, Chunk

class EmbeddingModel:
    """Generate vector embeddings for the text."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, chunks: list[Chunk]) -> list[Embedding]:
        """Generate embeddings for multiple chunks."""

        if not chunks:
            return []

        texts = [chunk.text for chunk in chunks]

        embeddings = self.model.encode(texts)

        return [
            Embedding(
                vector=vector.tolist(),
                dimension=len(vector),
            )
            for vector in embeddings
        ]