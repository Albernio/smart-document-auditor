from src.retrieval.answer_generator import LLMAnswerGenerator
from src.retrieval.llm.ollama_client import OllamaClient
from src.models import Chunk, SearchResult



def test_llm_answer_generator_with_real_ollama():
    client = OllamaClient(
        model_name="qwen3:8b",
    )

    generator = LLMAnswerGenerator(client)

    references = [
        SearchResult(
            chunk=Chunk(
                text="The provider must respond within thirty days.",
                index=0,
                document_hash="abc123",
            ),
            distance=0.1,
        )
    ]

    answer = generator.generate(
        question="How many days does the provider have to respond?",
        context="The provider must respond within thirty days.",
        references=references,
    )
    
    assert answer.text.strip()
    assert isinstance(answer.text, str)
    assert answer.references == references