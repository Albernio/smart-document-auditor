from src.persistence.database import get_connection

def create_tables() -> None:

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                CREATE EXTENSION IF NOT EXISTS vector;
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS documents(
                    id BIGSERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    hash_code TEXT NOT NULL UNIQUE,
                    size BIGINT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS document_chunks(
                    id BIGSERIAL PRIMARY KEY,
                    document_id BIGINT NOT NULL
                        REFERENCES documents(id)
                        ON DELETE CASCADE,
                    chunk_index INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    page_number INTEGER NOT NULL,
                    embedding vector(384) NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    UNIQUE (document_id, chunk_index)
                )
                """
            )

        connection.commit()
