from pathlib import Path
from src.models import Document, VectorRecord, Chunk, Embedding, SearchResult
from src.persistence.document_repository import DocumentRepository

import pytest



def test_save_document(database_connection):

    document_repository = DocumentRepository(database_connection)

    document_id = document_repository.save_document(
        Document(
            name="documento.pdf",
            path=Path("documento.pdf"),
            hash_code="abc123",
            size=1024,
            text="Document content",
        )
    )

    assert document_id > 0

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT name, hash_code, size
            FROM documents
            WHERE id=%s;
            """,
            (document_id,),
        )
        row = cursor.fetchone()

    assert row == (
        "documento.pdf",
        "abc123",
        1024,
    )

def test_save_vector_records(database_connection):

    document = Document(
        name="contract.pdf",
        path=Path("contract.pdf"),
        hash_code="def456",
        size=2048,
        text="Contract content",
    )

    records = [
        VectorRecord(
            Chunk(
                text="chunk_1",
                index=1,
                document_hash="def456"
            ),
            Embedding(
                vector=[1.0] + [0.0] * 383,
                dimension=384,
            )
        ),
        VectorRecord(
            Chunk(
                text="chunk_2",
                index=2,
                document_hash="def456"
            ),
            Embedding(
                vector=[0.0] + [1.0] + [0.0] * 382,
                dimension=384,
            )
        ),
    ]

    document_repository = DocumentRepository(database_connection)
    document_id = document_repository.save_document(document)

    document_repository.save_vector_records(document_id, records)

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT chunk_index, text, vector_dims(embedding)
            FROM document_chunks
            WHERE document_id=%s
            """,
            (document_id,),
        )
        rows = cursor.fetchall()
        print(rows)

    assert rows == [
        (
            1,
            "chunk_1",
            384
        ),
        (
            2,
            "chunk_2",
            384
        ),
    ]

def test_search_similar_returns_search_results(database_connection):

    repository = DocumentRepository(database_connection)

    document = Document(
        path=Path("contract.pdf"),
        name="contract.pdf",
        hash_code="abc123",
        size=1024,
    )

    document_id = repository.save_document(document)

    record = [
            VectorRecord(
                chunk=Chunk(
                    text="The provider must respond within thirty days.",
                    index=0,
                    document_hash=document.hash_code,
                ),
                embedding=Embedding(
                    vector=[1.0] + [0.0]*383,
                    dimension=384,
                ),
            ),
    ]

    repository.save_vector_records(document_id, record)

    results = repository.search_similar(
        query_embedding=[1.0] + [0.0]*383,
        limit=1,
    )

    assert len(results) == 1
    assert isinstance(results[0], SearchResult)
    assert isinstance(results[0].chunk, Chunk)
    assert isinstance(results[0].distance, float)

def test_search_similar_queries_return_similar_chunks(database_connection):

    repository = DocumentRepository(database_connection)

    document = Document(
        path=Path("contract.pdf"),
        name="contract.pdf",
        hash_code="abc123",
        size=1024,
    )

    document_id = repository.save_document(document)

    records = [
        VectorRecord(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=0,
                document_hash=document.hash_code,
            ),
            embedding=Embedding(
                vector=[1.0] + [0.0]*383,
                dimension=384,
            ),
        ),
        VectorRecord(
            chunk=Chunk(
                text="The supplier must protect personal data.",
                index=1,
                document_hash=document.hash_code,
            ),
            embedding=Embedding(
                vector=[0.0, 1.0] + [0.0]*382,
                dimension=384,
            ),
        ),
        VectorRecord(
            chunk=Chunk(
                text="The contract is valid for two years.",
                index=2,
                document_hash=document.hash_code,
            ),
            embedding=Embedding(
                vector=[0.0, 0.0, 1.0] + [0.0]*381,
                dimension=384,
            ),
        ),
    ]

    repository.save_vector_records(document_id, records)

    results = repository.search_similar(
        query_embedding=[1.0] + [0.0]*383,
        limit=3,
    )

    assert len(results) == 3

    assert results[0].chunk.text == (
        "The provider must respond within thirty days."
    )

def test_search_similar_preserves_document_hash(database_connection):

    repository = DocumentRepository(database_connection)

    document = Document(
        path=Path("contract.pdf"),
        name="contract.pdf",
        hash_code="hash_to_preserve",
        size=1024,
    )

    document_id = repository.save_document(document)

    record = [
        VectorRecord(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=0,
                document_hash=document.hash_code,
            ),
            embedding=Embedding(
                vector=[1.0] + [0.0]*383,
                dimension=384,
            ),
        ),
    ]

    repository.save_vector_records(document_id, record)

    results = repository.search_similar(
        query_embedding=[1.0] + [0.0]*383,
        limit=1,
    )

    assert results[0].chunk.document_hash == "hash_to_preserve"


def test_search_similar_respects_limit(database_connection):

    repository = DocumentRepository(database_connection)
    
    document = Document(
        path=Path("contract.pdf"),
        name="contract.pdf",
        hash_code="limit-test-document",
        size=1024,
    )

    document_id = repository.save_document(document)

    records = [
        VectorRecord(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=0,
                document_hash=document.hash_code,
            ),
            embedding=Embedding(
                vector=[1.0] + [0.0]*383,
                dimension=384,
            ),
        ),
        VectorRecord(
            chunk=Chunk(
                text="The supplier must protect personal data.",
                index=1,
                document_hash=document.hash_code,
            ),
            embedding=Embedding(
                vector=[0.0, 1.0] + [0.0]*382,
                dimension=384,
            ),
        ),
        VectorRecord(
            chunk=Chunk(
                text="The contract is valid for two years.",
                index=2,
                document_hash=document.hash_code,
            ),
            embedding=Embedding(
                vector=[0.0, 0.0, 1.0] + [0.0]*381,
                dimension=384,
            ),
        ),
    ]

    repository.save_vector_records(document_id, records)

    results = repository.search_similar([0.0, 1.0] + [0.0]*382, 2)

    assert len(results) == 2

def test_search_similar_rejects_limit(database_connection):
    
    repository = DocumentRepository(database_connection)

    with pytest.raises(
        ValueError, 
        match="Limit must be greater than 0.",
    ):
        repository.search_similar(
            query_embedding=[0.0]*384,
            limit=0,
        )


def test_search_similar_orders_by_distance(database_connection):

    repository = DocumentRepository(database_connection)
        
    document = Document(
        path=Path("contract.pdf"),
        name="contract.pdf",
        hash_code="distance-test-document",
        size=1024,
    )

    document_id = repository.save_document(document)

    records = [
        VectorRecord(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=0,
                document_hash=document.hash_code,
            ),
            embedding=Embedding(
                vector=[1.0] + [0.0]*383,
                dimension=384,
            ),
        ),
        VectorRecord(
            chunk=Chunk(
                text="The supplier must protect personal data.",
                index=1,
                document_hash=document.hash_code,
            ),
            embedding=Embedding(
                vector=[0.0, 1.0] + [0.0]*382,
                dimension=384,
            ),
        ),
    ]

    repository.save_vector_records(document_id, records)

    results = repository.search_similar(
        query_embedding=[1.0] + [0.0]*383,
        limit=2
    )

    assert results[0].distance <= results[1].distance
    assert results[0].chunk.index == 0