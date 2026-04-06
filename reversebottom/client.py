"""
Thin wrapper around OpenAI and Anthropic SDKs.
Exposes a single `complete(system, user) -> str` interface.
"""

from __future__ import annotations

from typing import Protocol

from .config import Provider, Settings, get_settings


class LLMClient(Protocol):
    def complete(self, system: str, user: str) -> str: ...


class OpenAIClient:
    def __init__(self, settings: Settings) -> None:
        from openai import OpenAI

        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.model
        self._temperature = settings.temperature
        self._max_tokens = settings.max_tokens

    def complete(self, system: str, user: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("OpenAI returned an empty response.")
        return content


class AnthropicClient:
    def __init__(self, settings: Settings) -> None:
        from anthropic import Anthropic

        self._client = Anthropic(api_key=settings.anthropic_api_key)
        self._model = settings.model
        self._temperature = settings.temperature
        self._max_tokens = settings.max_tokens

    def complete(self, system: str, user: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        block = response.content[0]
        if block.type != "text":
            raise RuntimeError(f"Unexpected Anthropic response block type: {block.type}")
        return block.text


def build_client(settings: Settings | None = None) -> LLMClient:
    cfg = settings or get_settings()
    if cfg.provider == Provider.OPENAI:
        return OpenAIClient(cfg)
    return AnthropicClient(cfg)
