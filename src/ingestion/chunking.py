from src.models import Chunk, Document


def validate_chunking(chunk_size: int, chunk_overlap: int) -> None:
    """Validates that chunk size and chunk overlap."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must not be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_size must be greater than chunk_overlap")


def chunk_text(
        document: Document,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
) -> list[Chunk]:
    """Split text into overlapping chunks."""

    validate_chunking(chunk_size, chunk_overlap)

    if document.pages == [(1, 0)]:
        return []

    step = chunk_size - chunk_overlap

    chunks = []
    chunk_index = 1

    for page in document.pages:

        text = page[1]

        for start in range(0, len(text), step):

            chnk_text = text[start:start + chunk_size]

            chunks.append(
                Chunk(
                    text=chnk_text,
                    index=chunk_index,
                    document_hash=document.hash_code,
                    page_number=page[0],
                )
            )

            chunk_index += 1

            if start + chunk_size >= len(text):
                break

    return chunks