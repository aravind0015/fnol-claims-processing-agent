from __future__ import annotations

from typing import Protocol


class LLMPort(Protocol):
    """Port for LLM text generation."""

    def generate(self, prompt: str) -> str: ...
