from __future__ import annotations

from google import genai

from application.ports.llm_port import LLMPort


class GeminiLLM(LLMPort):
    """
    Gemini adapter implementing the LLMPort.

    Note: API key is provided via constructor to avoid global state and allow swapping.
    """

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
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
