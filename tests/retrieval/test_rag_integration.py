from pathlib import Path

import pymupdf

from src.retrieval.rag import ask_question
from src.ingestion.embeddings import EmbeddingModel
from src.ingestion.ingestion import persist_document
from src.retrieval.llm.ollama_client import OllamaClient
from src.retrieval.answer_generator import LLMAnswerGenerator
from src.persistence.document_repository import DocumentRepository
from src.persistence.database import get_connection


def create_test_pdf(path: Path) -> None:
    """Create a PDF containing searchable contract text."""

    with pymupdf.open() as pdf:
        page = pdf.new_page()

        page.insert_text(
            (100, 750),
            "The provider must respond within thirty days.",
        )

        page.insert_text(
            (100, 700),
            "The supplier must protect personal data.",
        )

        page.insert_text(
            (100, 650),
            "The contract is valid for two years.",
        )

        pdf.save(path)


def test_rag_answers_question_using_real_documents_and_ollama(tmp_path):

    pdf_path = tmp_path / "contract.pdf"

    create_test_pdf(pdf_path)

    embedding_model = EmbeddingModel()

    persist_document(pdf_path, embedding_model)

    llm_client = OllamaClient(model_name="qwen3:8b")

    answer_generator = LLMAnswerGenerator(llm_client)

    with get_connection() as connection:

        repository = DocumentRepository(connection)

        answer = ask_question(
            question="How many days does the provider have to respond to complaints?",
            embedding_model=embedding_model,
            repository=repository,
            answer_generator=answer_generator,
            limit=3,
        )

    assert isinstance(answer.text, str)
    assert answer.text.strip()

    assert len(answer.references) > 0

    assert any(
        "thirty days" in reference.chunk.text.lower()
        for reference in answer.references
    )