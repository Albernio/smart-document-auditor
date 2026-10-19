from src.retrieval.answer_generator import LLMClient

class MockLLMClient(LLMClient):
    """Return a deterministic answer for tests."""

    def __init__(self) -> None:
        self.last_prompt = ""

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt

        return "The provider has thirty days to respond."