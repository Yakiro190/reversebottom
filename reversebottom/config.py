from enum import StrEnum
from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Provider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class Mode(StrEnum):
    DESTROY = "destroy"
    REVERSE = "reverse"
    SHADOW = "shadow"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Provider selection
    provider: Provider = Field(default=Provider.OPENAI, description="LLM provider to use")
    model: str = Field(default="gpt-4o", description="Model identifier")

    # Generation parameters
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=2048, ge=128, le=8192)

    # Default behavior
    default_mode: Mode = Field(default=Mode.DESTROY)

    # API keys (read from standard env vars, not RB_ prefix)
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")

    model_config = SettingsConfigDict(
        env_prefix="RB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
    )

    @model_validator(mode="after")
    def validate_api_key(self) -> "Settings":
        if self.provider == Provider.OPENAI and not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Export it or add it to your .env file."
            )
        if self.provider == Provider.ANTHROPIC and not self.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not set. Export it or add it to your .env file."
            )
        return self

    @property
    def active_api_key(self) -> str:
        if self.provider == Provider.OPENAI:
            return self.openai_api_key
        return self.anthropic_api_key


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
