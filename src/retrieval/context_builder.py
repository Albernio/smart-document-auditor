from src.models import SearchResult



def build_context(results: list[SearchResult]) -> str:
    """Build the context text that will be provided to the LLM."""

    if not results:
        return ""

    sections = []

    for result in results:
        sections.append(
            (
            f"Document: {result.chunk.document_hash} | "
            f"Chunk: {result.chunk.index}\n"
            f"{result.chunk.text}"
            )
        )

    return "\n\n".join(sections)