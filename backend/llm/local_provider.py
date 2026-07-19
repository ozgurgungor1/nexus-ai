import httpx

from backend.llm.provider_base import LLMProvider
from backend.core.config import settings


class LocalModelProvider(LLMProvider):
    def __init__(self) -> None:
        self.api_url = settings.local_model_api_url

    async def generate(self, prompt: str, model: str | None = None) -> str:
        if not self.api_url:
            raise RuntimeError("Local model API URL is not configured")
        payload = {"prompt": prompt, "max_tokens": 512}
        if model:
            payload["model"] = model
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.post(
                    self.api_url,
                    json=payload,
                )
                response.raise_for_status()
                return response.json().get("response", "")
            except httpx.HTTPError as exc:
                raise RuntimeError(f"Local model API bağlantısında hata oluştu: {exc}") from exc
