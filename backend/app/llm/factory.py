from app.llm.providers.ollama_provider import (
    OllamaProvider
)

from app.llm.providers.openai_provider import (
    OpenAIProvider
)

from app.llm.providers.gemini_provider import (
    GeminiProvider
)


def get_llm_provider(
    provider: str = "ollama"
):

    provider = provider.lower()

    if provider == "openai":

        return OpenAIProvider()

    if provider == "gemini":

        return GeminiProvider()

    return OllamaProvider()