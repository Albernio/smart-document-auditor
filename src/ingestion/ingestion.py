"""Orchestrates de document ingestion."""

from pathlib import Path

from src.ingestion import hashing, pdf_extraction, validation
from src.models import Document


def ingest_file(path: Path) -> Document:
    "Validate a file, create a hash and create a Document object."

    validation.validate_file(path)

    hash_code = hashing.calculate_hash(path)

    text = pdf_extraction.extract_text(path)

    return Document(
        path=path,
        name=path.name,
        hash_code=hash_code,
        size=path.stat().st_size,
        text=text,
    )