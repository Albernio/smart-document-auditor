"""Orchestrates de document ingestion."""

from pathlib import Path

from src.persistence.database import get_connection
from src.persistence.document_repository import DocumentRepository
from src.ingestion import hashing, pdf_extraction, validation
from src.ingestion.embeddings import EmbeddingModel
from src.ingestion.chunking import chunk_text
from src.models import Document


def ingest_document(path: Path) -> Document:
    "Validate a file, create a hash and create a Document object."

    validation.validate_file(path)

    hash_code = hashing.calculate_hash(path)

    pages = pdf_extraction.extract_text(path)

    return Document(
        path=path,
        name=path.name,
        hash_code=hash_code,
        size=path.stat().st_size,
        pages=pages,
    )

def persist_document(
        path: Path,
        embedding_model: EmbeddingModel,
    ) -> int:
    """Ingest a document and persist its chunks and embeddings."""

    document = ingest_document(path)

    chunks = chunk_text(document)

    records = embedding_model.create_vector_records(chunks)

    with get_connection() as connection:
        repository = DocumentRepository(connection)

        document_id = repository.save_document(document)

        repository.save_vector_records(document_id, records)

        connection.commit()
    
    return document_id