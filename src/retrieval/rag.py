from src.ingestion.embeddings import EmbeddingModel
from src.persistence.document_repository import DocumentRepository
from src.retrieval.answer_generator import AnswerGenerator
from src.retrieval.context_builder import build_context
from src.models import Answer
from src.retrieval.semantic_search import search_documents



def ask_question(
        question: str,
        embedding_model: EmbeddingModel,
        repository: DocumentRepository,
        answer_generator: AnswerGenerator,
        limit: int = 5,
) -> Answer:
    """Answer a question using the retrieved document context."""

    results = search_documents(
        query=question,
        embedding_model=embedding_model,
        repository=repository,
        limit=limit,
    )

    context = build_context(results)

    return answer_generator.generate(
        question=question,
        context=context,
        references=results,
    )