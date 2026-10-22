# Smart-document-auditor

A local application based on Retrieval-Augmented Generation (RAG) for analyzing PDF documents and answering questions using their content.

The system extracts text from PDF documents, splits it into chunks, generates vector embeddings, and stores them in PostgreSQL with pgvector. It retrieves semantically relevant chunks and uses a local LLM via Ollama to generate grounded answers with references to the source document.

# RAG Pipelines: Ingestion and Retrieval

This document describes the two main flows in
**Smart-document-auditor**: indexing PDF content and answering a user
query with retrieved context.

The diagrams reflect the repository's documented architecture: PDF text
extraction, chunking, embeddings, PostgreSQL with `pgvector`, semantic
retrieval, and a local Ollama LLM. Internal implementation details not
explicitly established by the public documentation are represented at a
conceptual level.

## 1. Ingestion flow

Ingestion prepares a PDF for semantic search. It extracts text, divides
it into chunks, computes an embedding for each chunk, and stores the
chunk and its vector in PostgreSQL.

``` mermaid
flowchart TD
    A([PDF document]) --> B[Validate input PDF]
    B --> C[Extract text with PyMuPDF]
    C --> D[Split extracted text into chunks]
    D --> E[Generate an embedding for each chunk]
    E --> F[(PostgreSQL + pgvector)]
    F --- G[Persist chunk text, metadata, and vector]
    G --> H([Document indexed for retrieval])
```

### Ingestion stages

1.  **Input** --- a PDF is supplied to the application.
2.  **Text extraction** --- PyMuPDF extracts text from the document's
    pages.
3.  **Chunking** --- extracted text is split into smaller passages
    suitable for retrieval.
4.  **Embedding generation** --- a sentence-transformer model converts
    each chunk into a vector.
5.  **Persistence** --- PostgreSQL stores chunk data and embeddings;
    `pgvector` enables vector similarity search.

## 2. Retrieval and answer-generation flow

Retrieval converts the user's question into an embedding, searches for
semantically similar chunks in PostgreSQL, and passes relevant context
to the local LLM to generate a grounded answer.

``` mermaid
flowchart TD
    A([User question]) --> B[Generate query embedding]
    B --> C[Semantic similarity search]
    C --> D[(PostgreSQL + pgvector)]
    D --> E[Return relevant chunks]
    E --> F[Build context from retrieved chunks]
    A --> G[Construct question and context prompt]
    F --> G
    G --> H[Local LLM via Ollama]
    H --> I[Generate answer grounded in retrieved context]
    I --> J[Return answer with document/page references]
    J --> K([User])
```

### Retrieval stages

1.  **Query embedding** --- the question is encoded using the embedding
    model used for document chunks.
2.  **Vector search** --- PostgreSQL with `pgvector` ranks stored chunks
    by vector distance and returns relevant results.
3.  **Context construction** --- selected chunks are assembled into the
    context supplied to the LLM.
4.  **Prompt construction** --- the prompt combines retrieved context
    with the user's question.
5.  **Answer generation** --- Ollama runs the local language model to
    produce an answer grounded in retrieved passages.
6.  **Response** --- the application returns the answer with document
    and page references where available.

## 3. How the two flows connect

``` mermaid
flowchart LR
    subgraph INGESTION["Document ingestion"]
        A[PDF] --> B[Extract text]
        B --> C[Chunk text]
        C --> D[Embed chunks]
        D --> DB[(PostgreSQL + pgvector)]
    end

    subgraph RETRIEVAL["Question answering"]
        Q[User question] --> QE[Embed question]
        QE --> VS[Vector similarity search]
        DB --> VS
        VS --> CTX[Retrieved context]
        CTX --> LLM[Ollama LLM]
        Q --> LLM
        LLM --> R[Answer with references]
    end
```

**Key distinction:** ingestion indexes document content ahead of time;
retrieval runs for each user question. Both flows meet at the vector
store.

## Components

  Component               Responsibility
  ----------------------- -----------------------------------------------------
  PyMuPDF                 Extracts text from PDF pages
  Sentence-transformers   Generates embeddings for chunks and queries
  PostgreSQL              Persists document/chunk data
  `pgvector`              Supports vector similarity search
  Ollama                  Runs the local language model for answer generation
  Streamlit               Provides the application UI

## Quick Start

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/Albernio/smart-document-auditor
cd smart-document-auditor
```

### 2. Set up the Python environment

The project requires **Python 3.13**. You can manage the environment and dependencies using `uv` (recommended) or `venv` and `pip`.

#### Option A: Use uv (recommended)

Install `uv` by following the instructions in its [official documentation](https://docs.astral.sh/uv/getting-started/installation/).

Check whether Python 3.13 is available, or let `uv` install it if necessary:

```bash
uv python install 3.13
```

Install the project dependencies, including development dependencies:

```bash
uv sync --extra test
```

This command creates or updates the `.venv` virtual environment, installs the dependencies declared in `pyproject.toml`, and keeps the `uv.lock` file synchronized.

Run project commands using `uv run`, for example:

```bash
uv run pytest -v
```

#### Option B: Use venv and pip

Make sure Python 3.13 is installed, then create the virtual environment:

```bash
python3.13 -m venv .venv
```

Activate the virtual environment.

**Linux / macOS:**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

Install the project and its development dependencies:

```bash
python -m pip install --upgrade pip
pip install -e ".[test]"
```

### 3. Start PostgreSQL + pgvector

You need to have **Docker installed and running**.

```bash
docker compose up -d
```

This starts PostgreSQL with the `pgvector` extension, according to the project's `compose.yaml` or `docker-compose.yml` configuration.

### 4. Create the database schema

If you are using `uv`:

```bash
uv run python -c "from src.schema import create_tables; create_tables()"
```

If you are using `venv` and `pip`, with the virtual environment activated:

```bash
python -c "from src.schema import create_tables; create_tables()"
```

This creates the required tables and enables the `vector` extension.

This step is only necessary when initializing the schema for a new database.

### 5. Run the application

If you are using `uv`:

```bash
uv run streamlit run app.py
```

If you are using `venv` and `pip`, with the virtual environment activated:

```bash
streamlit run app.py
```

Streamlit will display the local URL for accessing the application, usually `http://localhost:8501`.

### Notes

- **Python:** The project requires Python 3.13.
- **uv:** If you use this package manager, keep `uv.lock` in the repository to ensure reproducible dependency versions.
- **PostgreSQL:** The database service must be running, and its credentials must match the application's configuration.
- **Ollama:** You must have Ollama installed and running, and download the LLM model used by the project.
- **Configuration:** Review the environment variables and configuration files before starting the application.