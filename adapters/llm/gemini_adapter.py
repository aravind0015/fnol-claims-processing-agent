from __future__ import annotations

import os

from dotenv import load_dotenv
from google import genai

from ports.llm_port import LLMPort

load_dotenv(override=True)


class GeminiLLM(LLMPort):
    """
    Gemini adapter implementing the LLMPort.

    API key is always loaded from .env / environment at runtime.
    """

    def __init__(self, model: str = "gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not found in environment")

        print("Using Gemini key:", api_key[:6], "...")

        self._client = genai.Client(api_key=api_key)
        self._model = model

    def generate(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config={
                "temperature": 0,
                "response_mime_type": "application/json",
            },
        )
        return (response.text or "").strip()
