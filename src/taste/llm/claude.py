"""Claude/Anthropic LLM backend."""

from __future__ import annotations

import os
from dataclasses import dataclass

import anthropic

from taste.llm.backend import LLMBackend, LLMConfig


@dataclass
class ClaudeConfig(LLMConfig):
    model: str = "claude-sonnet-4-20250514"
    api_key: str = ""

    def build(self) -> ClaudeBackend:
        key = self.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            raise ValueError("Set ANTHROPIC_API_KEY or pass --llm.api_key")
        return ClaudeBackend(model=self.model, api_key=key, temperature=self.temperature, max_tokens=self.max_tokens)


class ClaudeBackend(LLMBackend):
    def __init__(self, model: str, api_key: str, temperature: float = 0.3, max_tokens: int = 8192):
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def complete(self, system: str, user: str) -> str:
        message = await self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return message.content[0].text
