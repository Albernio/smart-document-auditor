from src.retrieval.answer_generator import AnswerGenerator
from src.models import SearchResult, Answer



class MockAnswerGenerator(AnswerGenerator):
    """Generate deterministic answers for testing."""

    def generate(
            self,
            question: str,
            context: str,
            references: list[SearchResult]
    ) -> Answer:
        return Answer(
            text=f"Question: {question}\nContext: {context}",
            references=references,
        )