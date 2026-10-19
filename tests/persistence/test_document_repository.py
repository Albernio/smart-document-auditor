from pathlib import Path
from src.models import Document, VectorRecord, Chunk, Embedding
from src.persistence.document_repository import DocumentRepository



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