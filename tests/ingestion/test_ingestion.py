from src.ingestion.ingestion import ingest_document, persist_document
from src.ingestion.embeddings import EmbeddingModel
from src.ingestion.hashing import calculate_hash
from pathlib import Path

import pymupdf
import pytest

def create_test_pdf(path: Path, pages: list[str]):

    doc = pymupdf.open()

    for text in pages:
        page = doc.new_page()

        rect = pymupdf.Rect(
                50,
                50,
                page.rect.width - 50,
                page.rect.height - 50
        )
        page.insert_textbox(rect, text, fontsize=12)

    doc.save(path)
    doc.close()

def test_ingest_document_creates_document(tmp_path):

    path = tmp_path / "document.pdf"

    create_test_pdf(path, ["contenido de prueba"])

    document = ingest_document(path)

    assert document.path == path
    assert document.name == "document.pdf"
    assert document.hash_code
    assert document.size > 0
    assert any(
        "contenido de prueba" in text
        for _, text in document.pages
    )

def test_ingest_document_rejects_non_pdf(tmp_path):

    path = tmp_path / "document.txt"
    path.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="File is not a PDF"):
        ingest_document(path)

def test_ingest_document_rejects_empty_file(tmp_path):

    path = tmp_path / "document.pdf"
    path.touch()

    with pytest.raises(ValueError, match="PDF file is empty"):
        ingest_document(path)

def test_ingest_document_rejects_missing_file(tmp_path):

    path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        ingest_document(path)

def test_ingest_document_accepts_pdf_without_text(tmp_path):
    path = tmp_path / "no_text.pdf"
    create_test_pdf(path, [""])

    document = ingest_document(path)

    assert document.path == path
    assert document.name == "no_text.pdf"
    assert document.hash_code
    assert document.size > 0

    assert len(document.pages) == 1
    assert document.pages[0][1] == ""

def test_persist_document(tmp_path):
    path = tmp_path / "documento.pdf"

    create_test_pdf(path, ["This is the content of page 1", "This is the content of page 2"])

    document_id = persist_document(path, EmbeddingModel())

    assert document_id > 0

def test_persist_document_persists_chunks(tmp_path, database_connection):
    path = tmp_path / "documento.pdf"

    create_test_pdf(path, ["This is the content of page 1", "This is the content of page 2"])

    document_id = persist_document(path, EmbeddingModel())

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM document_chunks
            WHERE document_id=%s;
            """,
            (document_id,),
        )
        result = cursor.fetchone()

    assert result[0] > 0

def test_persist_document_persists_document_metadata(tmp_path, database_connection):
    path = tmp_path / "documento.pdf"

    create_test_pdf(path, ["This is the content of page 1", "This is the content of page 2"])

    expected_hash = calculate_hash(path)
    expected_size = path.stat().st_size

    document_id = persist_document(path, EmbeddingModel())

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT name, hash_code, size
            FROM documents
            WHERE id=%s;
            """,
            (document_id,),
        )
        result = cursor.fetchone()

    assert result == (
        "documento.pdf",
        expected_hash,
        expected_size
    )

def test_persist_document_persists_page_number(tmp_path, database_connection):
    path = tmp_path / "documento.pdf"

    create_test_pdf(path, ["This is the content of page 1", "This is the content of page 2"])

    document_id = persist_document(path, EmbeddingModel())
    
    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT page_number
            FROM document_chunks
            WHERE document_id=%s;
            """,
            (document_id,),
        )
        result = cursor.fetchall()

    assert result[0][0] == 1
    assert result[1][0] == 2