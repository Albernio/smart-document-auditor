from src.ingestion.ingestion import ingest_file
from src.models import Document
from hashlib import sha256
from pathlib import Path

import pymupdf

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
