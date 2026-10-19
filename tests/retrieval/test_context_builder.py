from src.models import SearchResult, Chunk
from src.retrieval.context_builder import build_context



def test_build_context():

    results = [
        SearchResult(
            Chunk(
                "Contenido del chunk 1",
                1,
                "abc123",
            ),
            0.3
        ),
        SearchResult(
            Chunk(
                "Contenido del chunk 2",
                2,
                "abc123",
            ),
            0.1
        ),
    ]

    context = build_context(results)

    assert "Contenido del chunk 1" in context
    assert "Contenido del chunk 2" in context

def test_build_context_empty_results_return_empty_string():

    results = []

    assert build_context(results) == ""