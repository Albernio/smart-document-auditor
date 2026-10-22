from pathlib import Path
import pymupdf

from src.ingestion.pdf_extraction import extract_text


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


def test_text_extraction_one_page(tmp_path):

    path = tmp_path / "document.pdf"

    create_test_pdf(path, ["contenido de prueba"])

    pages = extract_text(path)

    assert any(
        "contenido de prueba" in text
        for _, text in pages
    )

def test_text_extraction_several_pages(tmp_path):

    path = tmp_path / "document.pdf"
    
    create_test_pdf(
        path,
        [
            "contenido pagina 1",
            "contenido pagina 2",
            "contenido pagina 3",
        ],
    )

    pages = extract_text(path)
    
    assert any(
            "contenido pagina 1" in text
            for _, text in pages
        )
    assert any(
            "contenido pagina 2" in text
            for _, text in pages
        )
    assert any(
            "contenido pagina 3" in text
            for _, text in pages
        )