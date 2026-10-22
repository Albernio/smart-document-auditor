from src.ingestion.chunking import chunk_text
from src.models import Document

import pytest


def test_emtpy_text_returns_no_chunks():

    document = Document(
        path="contract.pdf",
        name="contract.pdf",
        hash_code="abc123",
        size=1024,
        pages=[(1,""),]
    )

    chunks = chunk_text(document)

    assert chunks == []

def test_short_text_returns_one_chunk():

    document = Document(
        path="contract.pdf",
        name="contract.pdf",
        hash_code="abc123",
        size=1024,
        pages=[(1,"hello world"),]
    )

    chunks = chunk_text(
        document,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert len(chunks) == 1
    assert chunks[0].text == "hello world"
    assert chunks[0].document_hash == "abc123"
    assert chunks[0].index == 1

def test_long_text_returns_multiple_chunks():

    document = Document(
        path="contract.pdf",
        name="contract.pdf",
        hash_code="abc123",
        size=1024,
        pages=[(1, "A" * 2500),]
    )

    chunks = chunk_text(document)

    assert len(chunks) == 3

def test_chunks_have_expected_overlap():

    document = Document(
        path="contract.pdf",
        name="contract.pdf",
        hash_code="abc123",
        size=1024,
        pages=[(1, "0123456789" * 300),]
    )

    chunks = chunk_text(
        document,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert chunks[0].text[-20:] == chunks[1].text[:20]
    assert chunks[1].text[-20:] == chunks[2].text[:20]
    assert chunks[2].text[-20:] == chunks[3].text[:20]

def test_chunk_size_must_be_positive():

    document = Document(
        path="contract.pdf",
        name="contract.pdf",
        hash_code="abc123",
        size=1024,
        pages=[(1,""),]
    )

    with pytest.raises(ValueError, match="chunk_size must be greater than 0"):
        chunk_text(document, chunk_size=0)

def test_chunk_overlap_cannot_be_negative():

    document = Document(
        path="contract.pdf",
        name="contract.pdf",
        hash_code="abc123",
        size=1024,
        pages=[(1,""),]
    )

    with pytest.raises(ValueError, match="chunk_overlap must not be negative"):
        chunk_text(document, chunk_overlap=-1)

def test_chunk_size_must_be_greater_than_overlap():

    document = Document(
        path="contract.pdf",
        name="contract.pdf",
        hash_code="abc123",
        size=1024,
        pages=[(1,""),]
    )

    with pytest.raises(ValueError, match="chunk_size must be greater than chunk_overlap"):
        chunk_text(document, chunk_size=10, chunk_overlap=10)

def test_chunk_text_preserves_page_number(tmp_path):

    chunks = chunk_text(
            Document(
                name="documento.pdf",
                path= tmp_path / "documento.pdf",
                hash_code="abc_123",
                size=1024,
                pages=[[1, "A"*500], [2, "B"*500],],
            )
        )

    assert len(chunks) == 2

    assert chunks[0].page_number == 1
    assert chunks[1].page_number == 2