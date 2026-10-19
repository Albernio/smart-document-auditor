from abc import ABC, abstractmethod

from src.models import SearchResult, Answer
from src.retrieval.prompts import build_prompt



class AnswerGenerator(ABC):
    """"Generate an answer from retrieved document context."""

    @abstractmethod
    def generate(
        self,
        question: str,
        context: str,
        references: list[SearchResult]
    ) -> Answer:
        "Generate an answer using the provided context."
        raise NotImplementedError

class LLMClient(ABC):
    """Interface for a language model client."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text from a prompt."""
        raise NotImplementedError


class LLMAnswerGenerator(AnswerGenerator):
    """Generate document-grounded answers using an LLM"""

    def __init__(self, client: LLMClient) -> None:
        self.client = client

    def generate(
            self,
            question: str,
            context: str,
            references: list[SearchResult]
        ) -> Answer:
        """Generate an answer using the retrieved document context."""

        prompt = build_prompt(
            question=question,
            context=context,
        )

        text = self.client.generate(prompt)

        return Answer(
            text=text,
            references=references,
        )