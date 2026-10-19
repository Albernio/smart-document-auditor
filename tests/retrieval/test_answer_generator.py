from tests.retrieval.fakes.mock_answer_generator import MockAnswerGenerator
from tests.retrieval.fakes.mock_llm_client import MockLLMClient
from src.retrieval.answer_generator import LLMAnswerGenerator
from src.models import Chunk, SearchResult



def test_mock_answer_generator_returns_answer():
    generator = MockAnswerGenerator()

    references = [
        SearchResult(
            Chunk(
                "Chunk 1",
                1,
                "abc123"
            ),
            0.5
        ),
        SearchResult(
            Chunk(
                "Chunk 2",
                2,
                "abc123"
            ),
            0.3
        ),
    ]

    answer = generator.generate(
        "How many days until the contract is terminated?",
        "The contract will be terminated in 30 days.",
        references=references,
    )

    assert answer.text
    assert answer.references == references

def test_llm_answer_generator_returns_answer():
    client = MockLLMClient()
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

    assert answer.text == "The provider has thirty days to respond."
    assert answer.references == references

def test_llm_answer_generator_sends_prompt_to_client():
    client = MockLLMClient()
    generator = LLMAnswerGenerator(client)

    generator.generate(
        question="How many days does the provider have to respond?",
        context="The provider must respond within thirty days.",
        references=[],
    )

    assert (
        "How many days does the provider have to respond?"
        in client.last_prompt
    )

    assert (
        "The provider must respond within thirty days."
        in client.last_prompt
    )

    assert (
        "Do not invent facts, dates, obligations, or references."
        in client.last_prompt
    )