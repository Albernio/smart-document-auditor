"""Extracts data from the PDF files."""

from pathlib import Path
import pymupdf
import pytesseract
from PIL import Image
from io import BytesIO


def extract_pages(path: Path) -> list[tuple[int, str]]:

    with pymupdf.open(path) as file:
        if all(page.get_text().strip() == "" for page in file):
            # Caso solo imágenes
            return extract_text_from_images(path)
        else:
            if any(page.get_images() for page in file):
                # Caso mixto
                return extract_text_from_mixed_pdf(path)
            else:
                # Caso solo texto
                return extract_text(path)

def extract_text(path: Path) -> list[tuple[int, str]]:
    """Extracts all the pages from an all text PDF file."""
    
    pages = []

    with pymupdf.open(path) as file:
        for page_number, text in enumerate(file, start=1):
            pages.append((page_number, text.get_text()))

    return pages

def extract_text_from_images(path: Path) -> list[tuple[int, str]]:
    """Extracts all the pages from a scanned PDF file."""

    pages = []

    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            # Render the PDF page as an image at 300 DPI.
            pixmap = page.get_pixmap(dpi=300)

            # Convert the rendered image to a PIL image.
            image = Image.frombytes(
                "RGB",
                (pixmap.width, pixmap.height),
                pixmap.samples,
            )

            # Extract text in English and Spanish.
            text = pytesseract.image_to_string(
                image,
                lang="eng+spa",
            )

            pages.append((page_number, text.strip()))

    return pages


def extract_text_from_mixed_pdf(path: Path) -> list[tuple[int, str]]:
    """Extract text and image text from a PDF, preserving reading order."""
    pages = []

    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            elements = []

            # Extract native text blocks with their page coordinates.
            page_dict = page.get_text("dict")

            for block in page_dict["blocks"]:
                if block["type"] == 0:
                    text = "".join(
                        span["text"]
                        for line in block["lines"]
                        for span in line["spans"]
                    ).strip()

                    if text:
                        x0, y0, _, _ = block["bbox"]
                        elements.append((y0, x0, text))

                elif block["type"] == 1:
                    # OCR embedded images.
                    x0, y0, _, _ = block["bbox"]
                    image_bytes = block.get("image")

                    if not image_bytes:
                        continue

                    image = Image.open(BytesIO(image_bytes)).convert("RGB")
                    text = pytesseract.image_to_string(
                        image,
                        lang="eng+spa",
                    ).strip()

                    if text:
                        elements.append((y0, x0, text))

            # Sort approximately by top-to-bottom, then left-to-right.
            elements.sort(key=lambda element: (element[0], element[1]))

            page_text = "\n".join(
                text for _, _, text in elements
            )

            pages.append((page_number, page_text))

    return pages