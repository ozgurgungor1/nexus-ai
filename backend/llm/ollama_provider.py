import httpx

from backend.llm.provider_base import LLMProvider
from backend.core.config import settings


class OllamaProvider(LLMProvider):
    def __init__(self) -> None:
        self.base_url = settings.ollama_url.rstrip("/") if settings.ollama_url else ""

    async def generate(self, prompt: str, model: str | None = None) -> str:
        if not self.base_url:
            raise RuntimeError("Ollama URL is not configured. Set ollama_url in .env or OLLAMA_URL environment variable.")
        model_name = model or "llama2"
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={"model": model_name, "prompt": prompt, "max_tokens": 512},
                )
                response.raise_for_status()
                return response.json().get("response", "")
            except httpx.HTTPError as exc:
                raise RuntimeError(f"Ollama sağlayıcısına bağlanırken hata oluştu: {exc}") from exc
