from src.models import Chunk, Embedding
from src.ingestion.embedding import EmbeddingModel


def test_embedding_model_returns_embeddings_list():

    model = EmbeddingModel()

    embeddings = model.encode([
        Chunk(
            text="chunk uno",
            index=1,
            document_hash="abc123",
        ),
        Chunk(
            text="chunk dos",
            index=2,
            document_hash="abc123",
        ),
        ]
    )

    assert isinstance(embeddings[0], Embedding)
    assert isinstance(embeddings[1], Embedding)

def test_embeddings_have_expected_dimension():

    model = EmbeddingModel()

    embeddings = model.encode([
        Chunk(
            text="chunk uno",
            index=1,
            document_hash="abc123",
        ),
        Chunk(
            text="chunk dos",
            index=2,
            document_hash="abc123",
        ),
        ]
    )

    print("Embedding 1 dimension:", embeddings[0].dimension)
    print("Embedding 2 dimension:", embeddings[1].dimension)

    assert embeddings[0].dimension > 0
    assert embeddings[1].dimension > 0

def test_similar_texts_have_similar_embeddings():
     
    model = EmbeddingModel()
    
    embeddings = model.encode([
            Chunk(
                text="El suministrador tiene 30 dias para responder",
                index=1,
                document_hash="abc123",
            )
        ]
    )

    embeddings2 = model.encode([
            Chunk(
                text="El proveedor tiene 30 dias para responder.",
                index=1,
                document_hash="abc1234",
            )
        ]
    )

    assert len(embeddings[0].vector) == len(embeddings2[0].vector)