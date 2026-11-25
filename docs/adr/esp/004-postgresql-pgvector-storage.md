# ADR-004: Uso de PostgreSQL + pgvector como almacén vectorial

## Contexto

El sistema RAG necesita almacenamiento persistente para los fragmentos de documentos y sus embeddings, además de la capacidad de realizar búsquedas por similitud durante la recuperación.

## Alternativas

- PostgreSQL + pgvector
- Bases de datos vectoriales dedicadas, como Qdrant, Milvus o Weaviate
- Índices vectoriales locales, como FAISS

## Decisión

Usaré PostgreSQL con la extensión pgvector como capa de persistencia y recuperación vectorial.

PostgreSQL almacenará tanto los metadatos estructurados de los documentos como los vectores de embeddings.

Pgvector permitirá realizar búsquedas de similitud vectorial directamente en PostgreSQL.

## Justificación

- Una sola base de datos para los metadatos y los vectores.
- PostgreSQL es una base de datos relacional madura y ampliamente utilizada.
- Menor complejidad arquitectónica para la escala del proyecto.
