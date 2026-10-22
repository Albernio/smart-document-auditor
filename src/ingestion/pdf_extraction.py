"""Extracts data from the PDF files."""

from pathlib import Path
import pymupdf


def extract_text(path: Path) -> list[tuple[int, str]]:
    """Extracts all the pages from a PDF file."""
    
    pages = []

    with pymupdf.open(path) as file:
        for page_number, text in enumerate(file, start=1):
            pages.append((page_number, text.get_text()))

    return pages