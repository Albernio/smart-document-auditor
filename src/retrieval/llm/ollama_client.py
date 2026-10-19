from ollama import Client

from src.retrieval.answer_generator import LLMClient



class OllamaClient(LLMClient):
    """LLM client backed by a local Ollama instance."""

    def __init__(
            self,
            model_name: str = "qwen3:8b",
            host: str = "http://localhost:11434",
            client: Client | None = None,
    ) -> None:
        self.model_name = model_name
        self.client = client or Client(host=host)

    def generate(self, prompt: str) -> str:
        """Generate text using the configured Ollama model."""

        response = self.client.chat(
            model=self.model_name,
            messages=[{
                "role":"user",
                "content":prompt,
            }
            ],
        )

        return response["message"]["content"]