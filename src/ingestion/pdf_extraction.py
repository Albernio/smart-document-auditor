"""Extracts data from the PDF files."""

from pathlib import Path
import pymupdf


def extract_text(path: Path) -> str:
    """Extracts all the text from a PDF file."""

    text = []

    with pymupdf.open(path) as file:
        for page in file:
            text.append(page.get_text())

    return "\n".join(text)