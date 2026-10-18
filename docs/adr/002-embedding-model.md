# ADR-003: Embedding Model

## Context

It is necessary to assign numerical vectors to chunks of text. For this reason, the system will need an embedding model.

## Alternatives

- **all-MiniLM-L6-v2** - English oriented - ~22M parameters
- **paraphrase-multilingual-MiniLM-L12-v2** - Multilingual - ~118M parameters
- **multilingual-e5-small**	- Multilingual - ~118M parameters
- **bge-m3** - Multilingual - ~568M parameters

## Decision

**paraphrase-multilingual-MiniLM-L12-v2** seems to be the simplest multilingual model, so it will be a good starting model for Embeddings.

## Motive

For a first version of the MVP, we don't need anything more elaborate.