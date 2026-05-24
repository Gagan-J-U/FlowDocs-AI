import os

from openai import OpenAI

from app.llm.providers.base import (
    BaseLLMProvider
)


class OpenAIProvider(
    BaseLLMProvider
):

    def __init__(
        self,
        model: str = "gpt-4o-mini"
    ):

        self.model = model

        self.client = OpenAI(

            api_key=os.getenv(
                "OPENAI_API_KEY"
            )
        )

    def generate(

        self,

        prompt: str,

        temperature: float = 0.2
    ) -> str:

        response = self.client.chat.completions.create(

            model=self.model,

            temperature=temperature,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    def stream(

        self,

        prompt: str,

        temperature: float = 0.2
    ):

        response = self.client.chat.completions.create(

            model=self.model,

            temperature=temperature,

            stream=True,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        for chunk in response:

            delta = chunk.choices[0].delta

            if delta.content:

                yield delta.content