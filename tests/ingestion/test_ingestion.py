from src.ingestion.ingestion import ingest_file
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

def test_ingest_file_creates_document(tmp_path):

    path = tmp_path / "document.pdf"

    create_test_pdf(path, ["contenido de prueba"])

    document = ingest_file(path)

    assert document.path == path
    assert document.name == "document.pdf"
    assert document.hash_code
    assert document.size > 0
    assert "contenido de prueba" in document.text

def test_ingest_file_rejects_non_pdf(tmp_path):

    path = tmp_path / "document.txt"
    path.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="File is not a PDF"):
        ingest_file(path)

def test_ingest_file_rejects_empty_file(tmp_path):

    path = tmp_path / "document.pdf"
    path.touch()

    with pytest.raises(ValueError, match="PDF file is empty"):
        ingest_file(path)

def test_ingest_file_rejects_missing_file(tmp_path):

    path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        ingest_file(path)

def test_ingest_file_accepts_pdf_without_text(tmp_path):
    path = tmp_path / "no_text.pdf"
    create_test_pdf(path, [""])

    document = ingest_file(path)

    assert document.path == path
    assert document.name == "no_text.pdf"
    assert document.hash_code
    assert document.size > 0
    assert document.text == ""