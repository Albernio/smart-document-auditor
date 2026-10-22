from src.retrieval.semantic_search import search_documents
from src.models import Chunk, SearchResult



class FakeEmbeddingModel:
    def encode(self, text: str) -> list[float]:
        assert text == "What is the response deadline?"

        return [1.0, 0.0]


class FakeRepository:
    def search_similar(
        self,
        query_embedding: list[float],
        limit: int,
    ) -> list[SearchResult]:

        assert query_embedding == [1.0, 0.0]
        assert limit == 5

        return [
            SearchResult(
                chunk=Chunk(
                    text="The provider must respond within thirty days.",
                    index=0,
                    document_hash="abc123",
                ),
                distance=0.0,
            )
        ]


def test_search_documents_returns_similar_chunks() -> None:
    embedding_model = FakeEmbeddingModel()
    repository = FakeRepository()

    results = search_documents(
        query="What is the response deadline?",
        embedding_model=embedding_model,
        repository=repository,
        limit=5,
    )

    assert len(results) == 1
    assert results[0].chunk.text == (
        "The provider must respond within thirty days."
    )