from src.ingestion.chunking import chunk_text, chunk_document
from src.models import Document

import pytest


def test_emtpy_text_returns_no_chunks():
    chunks = chunk_text("", document_hash="abc_123")

    assert chunks == []

def test_short_text_returns_one_chunk():

    text = "hello world"

    chunks = chunk_text(
        text,
        document_hash="abc_123",
        chunk_size=100,
        chunk_overlap=20,
    )

    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].document_hash == "abc_123"
    assert chunks[0].index == 0

def test_long_text_returns_multiple_chunks():

    text = "A" * 2500

    chunks = chunk_text(
        text,
        document_hash="abc123"
    )

    assert len(chunks) == 3

def test_chunks_have_expected_overlap():

    text = "0123456789" * 300

    chunks = chunk_text(
        text,
        document_hash="abc123",
        chunk_size=100,
        chunk_overlap=20,
    )

    assert chunks[0].text[-20:] == chunks[1].text[:20]
    assert chunks[1].text[-20:] == chunks[2].text[:20]
    assert chunks[2].text[-20:] == chunks[3].text[:20]

def test_chunk_size_must_be_positive():

    with pytest.raises(ValueError, match="chunk_size must be greater than 0"):
        chunk_text("hello", "abc123", chunk_size=0)

def test_chunk_overlap_cannot_be_negative():

    with pytest.raises(ValueError, match="chunk_overlap must not be negative"):
        chunk_text("hello", "abc123", chunk_overlap=-1)

def test_chunk_size_must_be_greater_than_overlap():

    with pytest.raises(ValueError, match="chunk_size must be greater than chunk_overlap"):
        chunk_text("hello", "abc123", chunk_size=10, chunk_overlap=10)

def test_chunk_document_returns_chunks(tmp_path):

    chunks = chunk_document(
        Document(
            name="documento.pdf",
            path= tmp_path / "documento.pdf",
            hash_code="abc_123",
            size=1024,
            text="A"*1500
        )
    )

    assert len(chunks) == 2