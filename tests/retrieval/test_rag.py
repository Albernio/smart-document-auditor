from unittest.mock import Mock, patch

from src.retrieval.answer_generator import AnswerGenerator
from src.models import Answer, Chunk, SearchResult
from src.retrieval.rag import ask_question


def test_ask_question_orchestrates_rag_pipeline() -> None:
    results = [
        SearchResult(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=0,
                document_hash="abc123",
            ),
            distance=0.1,
        )
    ]

    embedding_model = Mock()
    repository = Mock()
    answer_generator = Mock(spec=AnswerGenerator)

    answer_generator.generate.return_value = Answer(
        text="The provider has thirty days to respond.",
        references=results,
    )

    with (
        patch("src.retrieval.rag.search_documents", return_value=results) as search_mock,
        patch(
            "src.retrieval.rag.build_context",
            return_value="The provider must respond within thirty days.",
        ) as context_mock,
    ):
        answer = ask_question(
            question="How many days does the provider have to respond?",
            embedding_model=embedding_model,
            repository=repository,
            answer_generator=answer_generator,
            limit=5,
        )

    search_mock.assert_called_once_with(
        query="How many days does the provider have to respond?",
        embedding_model=embedding_model,
        repository=repository,
        limit=5,
    )

    context_mock.assert_called_once_with(results)

    answer_generator.generate.assert_called_once_with(
        question="How many days does the provider have to respond?",
        context="The provider must respond within thirty days.",
        references=results,
    )

    assert answer.text == "The provider has thirty days to respond."
    assert answer.references == results