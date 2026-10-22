from unittest.mock import Mock

from src.models import Chunk, SearchResult
from src.retrieval.semantic_search import search_documents


class FakeEmbeddingModel:
    def __init__(self) -> None:
        self.model = Mock()
        self.model.encode.return_value = Mock(
            tolist=Mock(return_value=[1.0, 0.0])
        )


class FakeRepository:
    def __init__(self) -> None:
        self.search_similar = Mock(
            return_value=[
                SearchResult(
                    chunk=Chunk(
                        text="The provider must respond within thirty days.",
                        index=0,
                        document_hash="abc123",
                    ),
                    distance=0.0,
                )
            ]
        )


def test_search_documents_returns_similar_chunks() -> None:
    embedding_model = FakeEmbeddingModel()
    repository = FakeRepository()

    results = search_documents(
        query="What is the response deadline?",
        embedding_model=embedding_model,
        repository=repository,
        limit=5,
    )

    embedding_model.model.encode.assert_called_once_with(
        "What is the response deadline?"
    )

    repository.search_similar.assert_called_once_with(
        query_embedding=[1.0, 0.0],
        limit=5,
    )

    assert len(results) == 1
    assert results[0].chunk.text == (
        "The provider must respond within thirty days."
    )
    assert results[0].distance == 0.0