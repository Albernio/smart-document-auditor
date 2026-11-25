# ADR-002: División en fragmentos basada en caracteres

## Contexto

El sistema necesita una forma de dividir el texto en varios fragmentos que se transformarán en embeddings únicos para almacenarlos posteriormente como vectores.

## Alternativas

- División en fragmentos de tamaño fijo (basada en caracteres o tokens)
- División recursiva por caracteres
- División que tiene en cuenta la estructura o el diseño
- División semántica

## Decisión

He decidido usar la **división en fragmentos basada en caracteres** (de tamaño fijo) por su sencillez de implementación.

## Justificación

Para una primera versión del MVP, no necesitamos nada más elaborado.
