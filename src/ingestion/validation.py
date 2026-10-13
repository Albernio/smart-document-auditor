from pathlib import Path


def validate_file(path: Path) -> None:
    """Validates that the input is a non-empty PDF file."""

    if not path.exists():
        raise FileNotFoundError(f"File Not Found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"PDF file is empty: {path}")