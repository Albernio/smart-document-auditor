from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw, ImageFont

from src.ingestion.pdf_extraction import extract_text, extract_text_from_images, extract_text_from_mixed_pdf


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

def test_extract_text_from_image_only_pdf(tmp_path: Path) -> None:
    """Verify that OCR extracts known text from an image-only PDF."""
    image_path = tmp_path / "page.png"
    pdf_path = tmp_path / "scanned.pdf"

    # Create an image containing known text.
    image = Image.new("RGB", (1600, 400), "white")
    draw = ImageDraw.Draw(image)
    draw.text(
        (50, 100),
        "OCR TEST 12345",
        fill="black",
        font=ImageFont.truetype("DejaVuSans.ttf", 80),
    )
    image.save(image_path)

    # Embed the image in a PDF with no selectable text.
    with pymupdf.open() as document:
        page = document.new_page(width=800, height=200)
        page.insert_image(page.rect, filename=str(image_path))
        document.save(pdf_path)

    # Confirm that the PDF contains no selectable text.
    with pymupdf.open(pdf_path) as document:
        assert document[0].get_text().strip() == ""

    # Run real OCR
    result = extract_text_from_images(pdf_path)

    assert len(result) == 1
    assert result[0][0] == 1
    assert "OCR TEST 12345" in result[0][1].upper()


def test_mixed_pdf_preserves_text_and_image_order(
    tmp_path: Path,
) -> None:
    pdf_path = tmp_path / "mixed.pdf"
    image_path = tmp_path / "embedded_text.png"

    # Create an image containing recognizable text.
    image = Image.new("RGB", (1000, 180), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("DejaVuSans.ttf", 48)
    draw.text((20, 40), "TEXTO DENTRO DE IMAGEN", fill="black", font=font)
    image.save(image_path)

    # Create a PDF with native text, an image, and more native text.
    with pymupdf.open() as document:
        page = document.new_page(width=600, height=700)

        page.insert_text((50, 80), "INICIO DEL DOCUMENTO")

        page.insert_image(
            pymupdf.Rect(50, 130, 550, 220),
            filename=str(image_path),
        )

        page.insert_text((50, 280), "FIN DEL DOCUMENTO")

        document.save(pdf_path)

    # Run real extraction and OCR.
    result = extract_text_from_mixed_pdf(pdf_path)

    assert len(result) == 1
    assert result[0][0] == 1

    extracted_text = result[0][1]

    start_position = extracted_text.index("INICIO DEL DOCUMENTO")
    image_position = extracted_text.index("TEXTO DENTRO DE IMAGEN")
    end_position = extracted_text.index("FIN DEL DOCUMENTO")

    assert start_position < image_position < end_position