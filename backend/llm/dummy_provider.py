from backend.llm.provider_base import LLMProvider
from backend.core.config import settings


class DummyProvider(LLMProvider):
    async def generate(self, prompt: str, model: str | None = None) -> str:
        if settings.openai_api_key or settings.ollama_url or settings.local_model_api_url:
            return (
                "OpenAI, Ollama veya lokal model yapılandırılmış ancak şu anda yanıt veremiyor. "
                "Lütfen bağlantı/limit durumunu kontrol edin veya farklı bir sağlayıcı kullanın."
            )

        return (
            "OpenAI, Ollama veya lokal model yapılandırılmadı. "
            "Lütfen .env dosyanıza OPENAI_API_KEY, OLLAMA_URL veya LOCAL_MODEL_API_URL ekleyin."
        )
