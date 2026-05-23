from app.prompting.strategies.base import (
    BasePromptStrategy
)


class DefaultStrategy(
    BasePromptStrategy
):

    def build(

        self,

        query: str,

        chunks: list
    ):

        context_blocks = []

        for idx, chunk in enumerate(chunks):

            block = f"""
SOURCE {idx + 1}

Section:
{chunk.get("section_title", "Unknown")}

Pages:
{chunk.get("start_page")} to {chunk.get("end_page")}

Content:
{chunk["text"]}
"""

            context_blocks.append(
                block
            )

        context = "\n\n".join(
            context_blocks
        )

        return f"""
You are an accurate AI research assistant.

Your task is to answer the user's question using ONLY the provided document context.

Rules:
- Use only information from the context.
- Do not invent or assume facts.
- If the answer is partially available, clearly mention what is available.
- If the answer is not present in the context, respond with:
"I could not find the answer in the provided documents."
- Keep the answer factual, clear, and well-structured.
- Do not say phrases like:
  "According to the documents" unless necessary.
- Prefer direct explanations over copying sentences verbatim.

USER QUESTION:
{query}


DOCUMENT CONTEXT:
{context}


FINAL ANSWER:
"""