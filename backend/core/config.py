from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "NEXUS AI"
    environment: str = "development"
    database_url: str = Field(default="sqlite:///./data/nexus_ai.db")
    secret_key: str = Field(default="change-me-nexus-ai-secret")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    ollama_url: str = Field(default="", env="OLLAMA_URL")
    local_model_api_url: str = Field(default="", env="LOCAL_MODEL_API_URL")
    cors_origins: list[str] = Field(default=["*"], env="CORS_ORIGINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


settings = AppSettings()
