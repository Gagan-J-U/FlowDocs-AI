from app.llm.factory import (
    get_llm_provider
)


def summarize_document_context(

    chunks: list,

    provider="ollama"
):

    context = "\n\n".join(

        chunk["text"]

        for chunk in chunks
    )

    prompt = f"""
You are analyzing a document.

Summarize:

1. Main topics
2. Important concepts
3. Key arguments
4. Important findings

Document Context:

{context}
"""

    llm = get_llm_provider(
        provider
    )

    return llm.generate(
        prompt
    )