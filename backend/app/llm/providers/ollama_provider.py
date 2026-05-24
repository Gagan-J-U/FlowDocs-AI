import ollama

from app.llm.providers.base import (
    BaseLLMProvider
)


class OllamaProvider(
    BaseLLMProvider
):

    def __init__(
        self,
        model: str = "llama3"
    ):

        self.model = model

    def generate(
        self,
        prompt: str
    ) -> str:

        response = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    def stream(

        self,

        prompt: str,

        temperature: float = 0.2
    ):

        stream = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            stream=True,

            options={
                "temperature": temperature
            }
        )

        for chunk in stream:

            token = chunk["message"]["content"]

            yield token