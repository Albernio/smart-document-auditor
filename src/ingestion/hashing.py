from pathlib import Path
from hashlib import sha256


def calculate_hash(path: Path) -> str:
    """Generates a hash sha-256 from the content in a PDF file."""
    hash_code = sha256()

    with open(path, "rb") as file:
        while chunk := file.read(8192):
            hash_code.update(chunk)

    return hash_code.hexdigest()