from pydantic_settings import BaseSettings
from anthropic import AsyncAnthropic, Anthropic


class Settings(BaseSettings):
    environment: str = "dev"
    anthropic_api_key: str

    @property
    def claude_model(self) -> str:
        if self.environment == "dev":
            return "claude-3-5-haiku-20241022"
        else:
            return "claude-sonnet-4-5-20250929"

    @property
    def max_tokens(self) -> int:
        if self.environment == "dev":
            return 1024  # ~750 words
        else:
            return 4096  # ~3000 words

    class Config:
        env_file = ".env"


# instantiate once at module load
settings = Settings()

# for testing/scripts
synchronous_client = Anthropic(api_key=settings.anthropic_api_key)
# async for FastAPI endpoints
anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
