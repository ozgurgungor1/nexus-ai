import asyncio
import os

from openai import OpenAI, RateLimitError

from backend.llm.provider_base import LLMProvider
from backend.core.config import settings


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        self.api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")

    async def generate(self, prompt: str, model: str | None = None) -> str:
        if not self.api_key:
            raise RuntimeError(
                "OpenAI API key is not configured. Set OPENAI_API_KEY or openai_api_key in .env"
            )

        model_name = model or settings.openai_model or "gpt-3.5-turbo"

        def sync_call() -> str:
            try:
                client = OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=512,
                )
                return response.choices[0].message.content
            except RateLimitError as exc:
                raise RuntimeError(
                    "OpenAI rate limit exceeded. Lütfen daha sonra tekrar deneyin veya farklı bir sağlayıcı kullanın."
                ) from exc
            except Exception as exc:
                raise RuntimeError(f"OpenAI sağlayıcısı hatası: {exc}") from exc

        return await asyncio.to_thread(sync_call)
