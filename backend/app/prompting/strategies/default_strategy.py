from app.prompting.strategies.base import (
    BasePromptStrategy
)


class DefaultStrategy(
    BasePromptStrategy
):

    def build(

        self,

        query: str,

        chunks: list,

        figures=None
    ):
        figure_context = ""

        if figures:

            blocks = []

            for index, figure in enumerate(figures):

                blocks.append(
                    f"""
        [Figure {index + 1}]

        Figure ID:
        {figure["figure_id"]}

        Page:
        {figure["page_number"]}

        Caption:
        {figure["caption"]}
        """
                )

            figure_context = "\n".join(
                blocks
            )

        context_blocks = []

        for idx, chunk in enumerate(chunks):

            block = f"""
[{idx + 1}]

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
- If the answer is not present in the context, respond exactly with:
"I could not find the answer in the provided documents."
- Keep the answer factual, clear, and well-structured.
- Prefer direct explanations over copying sentences verbatim.
- Do not mention phrases like:
  "According to the documents"
  "Based on the provided context"
  unless absolutely necessary.
- Cite supporting sources inline using:
  [source_number]
- Only use citation numbers that exist in the provided context.
- Do NOT invent citations.
- Multiple citations are allowed.
  Example:
  Spyware can record user activity [1][3]
-When referring to a figure use:
[FIGURE:figure_id]
Example:
The architecture is shown in the network diagram
[FIGURE:a1b2c3]

QUESTION:
{query}


DOCUMENT CONTEXT:
{context}

AVAILABLE FIGURES:
{figure_context}


FINAL ANSWER:
"""