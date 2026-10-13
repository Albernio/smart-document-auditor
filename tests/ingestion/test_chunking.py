from src.ingestion.chunking import chunk_text

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