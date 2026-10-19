# ADR-005: First LLM for Answer Generation

## Context

The RAG system requires a generative language model to produce answers from retrieved document chunks. The system is intended to support multilingual documents and user queries.

## Decision

Use qwen3:8b through Ollama as the local generation model.

## Motive

- Local execution
- Multilingual capability
- Model size: The 8B model provides a practical compromise between generation quality and local resource requirements.
- Operational simplicity