import psycopg

from src.models import Document, VectorRecord, SearchResult, Chunk


class DocumentRepository:
    """Persist documents and their vector data."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def save_document(self, document: Document) -> int:
        """Save a document and return its database identifier."""

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (
                    name,
                    hash_code,
                    size
                )
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (
                    document.name,
                    document.hash_code,
                    document.size,
                ),
            )

            document_id = cursor.fetchone()[0]

        return document_id

    def save_vector_records(
            self,
            document_id: int,
            records: list[VectorRecord]
    ) -> None:
        """Save chunk and embedding records for a document."""

        if not records:
            return

        with self.connection.cursor() as cursor:
            for record in records:
                cursor.execute(
                    """
                    INSERT INTO document_chunks(
                        document_id,
                        chunk_index,
                        text,
                        page_number,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s, %s::vector);
                    """,
                    (
                        document_id,
                        record.chunk.index,
                        record.chunk.text,
                        record.chunk.page_number,
                        str(record.embedding.vector)
                    ),
                )

    def search_similar(
            self,
            query_embedding: list[float],
            limit: int = 5,
    ) -> list[SearchResult]:
        """Search for the most similar results"""

        if limit <= 0:
            raise ValueError("Limit must be greater than 0.")

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    dc.text,
                    dc.chunk_index,
                    d.hash_code,
                    dc.page_number,
                    dc.embedding <=> %s::vector AS distance
                FROM document_chunks AS dc
                JOIN documents AS d
                    ON dc.document_id = d.id
                    ORDER BY dc.embedding <=> %s::vector
                LIMIT %s;
                """,
                (
                    str(query_embedding),
                    str(query_embedding),
                    limit,
                ),
            )

            rows = cursor.fetchall()

        return [
            SearchResult(
                chunk = Chunk(
                    text=row[0],
                    index=row[1],
                    document_hash=row[2],
                    page_number=row[3],
                ),
                distance=float(row[3]),
            )
            for row in rows
        ]