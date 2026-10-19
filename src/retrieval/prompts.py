RAG_SYSTEM_PROMPT = """
You are a document analysis assistant.

Answer the user's question using only the provided context.

Rules:
- Do not use information that is not present in the context.
- If the context does not contain enough information to answer the question,
  say that there is not enough information in the provided documents.
- Do not invent facts, dates, obligations, or references.
- Answer clearly and concisely.

Context:
{context}

Question:
{question}
"""

def build_prompt(
        question: str,
        context: str,
) -> str:
    """Build the prompt used for RAG answer generation."""

    return RAG_SYSTEM_PROMPT.format(
        context=context,
        question=question
    )