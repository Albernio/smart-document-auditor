from src.models import Chunk


def chunk_text(
        text: str,
        document_hash: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
) -> list[Chunk]:
    """Split text into overlapping chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must not be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_size must be greater than chunk_overlap")

    if not text:
        return []

    step = chunk_size - chunk_overlap

    chunks = []

    for start in range(0, len(text), step):

        chnk_text = text[start:start + chunk_size]

        chunks.append(
            Chunk(
                text=chnk_text,
                index=len(chunks),
                document_hash=document_hash,
            )
        )

        if start + chunk_size >= len(text):
            break

    return chunks