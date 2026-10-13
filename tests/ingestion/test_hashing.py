from hashlib import sha256

from src.ingestion.hashing import calculate_hash


def test_calculate_hash(tmp_path):

    document = tmp_path / "document.pdf"
    document.write_bytes(b"contenido de prueba")

    assert calculate_hash(document) == sha256(b"contenido de prueba").hexdigest()

def test_calculate_hash_different_content_generates_different_hash(tmp_path):

    document = tmp_path / "document.pdf"
    document.write_bytes(b"contenido de prueba")

    hash_1 = calculate_hash(document)

    document.write_bytes(b"contenido adicional")

    hash_2 = calculate_hash(document)

    assert hash_1 != hash_2