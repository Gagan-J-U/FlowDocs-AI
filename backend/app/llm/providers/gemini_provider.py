import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.llm.providers.base import (
    BaseLLMProvider
)


class GeminiProvider(
    BaseLLMProvider
):

    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
    ):

        load_dotenv()

        self.model = model

        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )

        if not self.api_key:
            raise RuntimeError(
                "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY "
                "in your environment or pass api_key to GeminiProvider."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature
            )
        )

        return response.text
