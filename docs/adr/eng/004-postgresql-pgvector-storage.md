# ADR-004: Use of PostgreSQL + pgvector as the Vector store

## Context

The RAG system needs persistent storage for document chunks and their embeddings, together with the ability to perform similarity searches during the retrieval.

## Alternatives

- PostgreSQL + pgvector
- Dedicated vector databases such as Qdrant, Milvus or Weaviate.
- Local vector indexes such as FAISS

## Decision

I will use PostgreSQL with the pgvector extension as the persistence and vector-retrieval layer.

PostgreSQL will store both the structure document metadata and the embedding vectors.

Pgvector will provide vector similarity search directly inside PostgreSQL.

## Motive

- One database for metadata and vectors.
- PostgreSQL is a mature and widely used relational database.
- Lower architectural complexity for the project's scale.