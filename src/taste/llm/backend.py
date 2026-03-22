"""Abstract LLM backend interface."""

from __future__ import annotations

import abc
from dataclasses import dataclass


class LLMBackend(abc.ABC):
    @abc.abstractmethod
    async def complete(self, system: str, user: str) -> str:
        ...


@dataclass
class LLMConfig:
    """Base LLM config. Subclass for specific providers."""
    model: str = ""
    temperature: float = 0.3
    max_tokens: int = 8192

    @classmethod
    def get_default(cls) -> LLMConfig:
        from taste.llm.claude import ClaudeConfig
        return ClaudeConfig()

    def build(self) -> LLMBackend:
        raise NotImplementedError("Use a specific LLM config like ClaudeConfig")
