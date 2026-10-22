from pathlib import Path
import tempfile

import streamlit as st

from src.ingestion.embeddings import EmbeddingModel
from src.ingestion.ingestion import persist_document
from src.retrieval.answer_generator import LLMAnswerGenerator
from src.retrieval.llm.ollama_client import OllamaClient
from src.retrieval.rag import ask_question
from src.persistence.document_repository import DocumentRepository
from src.persistence.database import get_connection


st.set_page_config(
    page_title="Smart Document Auditor",
    page_icon="📄",
    layout="wide",
)

st.title("Smart Document Auditor")
st.write(
    "Upload documents and ask questions about their contents."
)


uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
)


if uploaded_file is not None:
    st.success(
        f"Document uploaded: {uploaded_file.name}"
    )

    if st.button("Ingest document"):
        with st.spinner("Processing document..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = Path(temp_dir) / uploaded_file.name

                file_path.write_bytes(
                    uploaded_file.getvalue()
                )

                embedding_model = EmbeddingModel()

                document_id = persist_document(
                    file_path,
                    embedding_model,
                )

        st.success(
            f"Document ingested successfully. "
            f"Document ID: {document_id}"
        )
        st.divider()

    st.subheader("Ask a question")

    question = st.text_input(
        "Question",
        placeholder="How many days does the provider have to respond?",
    )

    if st.button("Ask") and question:
        with st.spinner("Searching documents and generating answer..."):
            embedding_model = EmbeddingModel()
            ollama_client = OllamaClient(
                model_name="qwen3:8b",
            )
            answer_generator = LLMAnswerGenerator(
                ollama_client,
            )

            with get_connection() as connection:
                repository = DocumentRepository(connection)

                answer = ask_question(
                    question=question,
                    embedding_model=embedding_model,
                    repository=repository,
                    answer_generator=answer_generator,
                )

        st.subheader("Answer")
        st.write(answer.text)

        st.subheader("References")

        for reference in answer.references:
            chunk = reference.chunk

            st.write(
                f"- Document: `{chunk.document_hash}` | "
                f"- Page: `{chunk.page_number}` | "
                f"Chunk: `{chunk.index}`"
            )