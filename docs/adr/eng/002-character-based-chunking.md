# ADR-002: Character-based chunking

## Context

The system needs a way to divide the text into multiple chunks that will be transformed into unique embeddings for later persistence as vectors.

## Alternatives

- Fixed-Size Chunking (Character / Token-based)
- Recursive Character Chunking
- Structure / Layout-Aware Chunking
- Semantic Chunking

## Decision

I decided to use **Character-based chunking** (Fixed-size) for its simplicity to implement.

## Motive

For a first version of the MVP, we don't need anything more elaborate.