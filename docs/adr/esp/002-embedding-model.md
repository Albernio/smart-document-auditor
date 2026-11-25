# ADR-003: Modelo de embeddings

## Contexto

Es necesario asignar vectores numéricos a los fragmentos de texto. Por este motivo, el sistema necesita un modelo de embeddings.

## Alternativas

- **all-MiniLM-L6-v2** - Orientado al inglés - ~22 millones de parámetros
- **paraphrase-multilingual-MiniLM-L12-v2** - Multilingüe - ~118 millones de parámetros
- **multilingual-e5-small** - Multilingüe - ~118 millones de parámetros
- **bge-m3** - Multilingüe - ~568 millones de parámetros

## Decisión

**paraphrase-multilingual-MiniLM-L12-v2** parece ser el modelo multilingüe más sencillo, así que será un buen punto de partida para generar embeddings.

## Justificación

Para una primera versión del MVP, no necesitamos nada más elaborado.
