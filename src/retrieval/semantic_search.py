from src.ingestion.embeddings import EmbeddingModel
from src.models import SearchResult
from src.persistence.document_repository import DocumentRepository



def search_documents(
        query: str,
        embedding_model: EmbeddingModel,
        repository: DocumentRepository,
        limit: int = 5,
) -> list[SearchResult]:
    """Search documents using a natural-language query."""

    query_embedding = embedding_model.model.encode(query).tolist()

    return repository.search_similar(
        query_embedding=query_embedding,
        limit=limit,
    )