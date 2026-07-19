import os

from backend.llm.dummy_provider import DummyProvider
from backend.llm.local_provider import LocalModelProvider
from backend.llm.ollama_provider import OllamaProvider
from backend.llm.openai_provider import OpenAIProvider
from backend.core.config import settings


class AIService:
    def __init__(self) -> None:
        self._provider_classes = {
            "openai": OpenAIProvider,
            "ollama": OllamaProvider,
            "local": LocalModelProvider,
            "dummy": DummyProvider,
        }
        self._providers: dict[str, object] = {}

    async def generate(self, prompt: str, provider_name: str = "openai", model: str | None = None) -> str:
        if provider_name not in self._provider_classes:
            raise ValueError(f"Unknown provider: {provider_name}")

        last_exception: Exception | None = None
        for candidate in self._provider_order(provider_name):
            provider = self._get_provider(candidate)
            try:
                return await provider.generate(prompt, model=model)
            except Exception as exc:
                last_exception = exc
                continue

        error_message = str(last_exception) if last_exception else "No available LLM provider."
        raise RuntimeError(error_message)

    def _get_provider(self, provider_name: str) -> object:
        provider = self._providers.get(provider_name)
        if provider is None:
            provider = self._provider_classes[provider_name]()
            self._providers[provider_name] = provider
        return provider

    def _provider_order(self, provider_name: str) -> list[str]:
        order: list[str] = [provider_name]

        if provider_name == "openai":
            if settings.local_model_api_url:
                order.append("local")
            if settings.ollama_url:
                order.append("ollama")
        elif provider_name == "local":
            if self._has_openai_api_key():
                order.append("openai")
            if settings.ollama_url:
                order.append("ollama")
        elif provider_name == "ollama":
            if self._has_openai_api_key():
                order.append("openai")
            if settings.local_model_api_url:
                order.append("local")

        if "dummy" not in order:
            order.append("dummy")
        return order

    def select_provider(self, user_preference: str | None = None) -> str:
        if user_preference:
            preference = user_preference.lower()
            if "local" in preference:
                return "local"
            if "ollama" in preference or "llama" in preference:
                return "ollama"
            if "openai" in preference or "gpt" in preference or "chat" in preference:
                return "openai"

        if self._has_openai_api_key():
            return "openai"
        if settings.local_model_api_url:
            return "local"
        if settings.ollama_url:
            return "ollama"
        return "dummy"

    def _fallback_provider(self, provider_name: str, exc: Exception | None = None) -> str | None:
        if provider_name == "openai":
            if not self._has_openai_api_key():
                if settings.local_model_api_url:
                    return "local"
                if settings.ollama_url:
                    return "ollama"
                return "dummy"
            if isinstance(exc, RuntimeError):
                if settings.local_model_api_url:
                    return "local"
                if settings.ollama_url:
                    return "ollama"
                return "dummy"

        if provider_name == "local":
            if not settings.local_model_api_url:
                if self._has_openai_api_key():
                    return "openai"
                if settings.ollama_url:
                    return "ollama"
                return "dummy"
            if isinstance(exc, RuntimeError):
                if self._has_openai_api_key():
                    return "openai"
                if settings.ollama_url:
                    return "ollama"
                return "dummy"

        if provider_name == "ollama":
            if not settings.ollama_url:
                if self._has_openai_api_key():
                    return "openai"
                if settings.local_model_api_url:
                    return "local"
                return "dummy"
            if isinstance(exc, RuntimeError):
                if self._has_openai_api_key():
                    return "openai"
                if settings.local_model_api_url:
                    return "local"
                return "dummy"

        return None

    def _has_openai_api_key(self) -> bool:
        return bool(settings.openai_api_key or os.getenv("OPENAI_API_KEY"))
