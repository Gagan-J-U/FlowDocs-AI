from app.prompting.strategies.base import (
    BasePromptStrategy
)


class TeachingStrategy(
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
You are an expert educational AI tutor.

Your goal is to teach the concept clearly to a beginner using ONLY the provided document context as factual grounding.

Instructions:
- Explain concepts step-by-step in simple language.
- Give a detailed and beginner-friendly explanation.
- Explain technical terms when they are introduced.
- Use examples and analogies when useful.
- Teach naturally instead of summarizing the text directly.
- Expand ideas in your own words while remaining faithful to the context.
- Do not invent facts outside the provided context.
- Do not mention phrases like:
  "According to the documents"
  "Based on the provided context"
  unless absolutely necessary.
- If the context is insufficient, clearly state what information is missing.
- Cite supporting information inline using:
  [source_number]
- Only use citation numbers that exist in the provided context.
- Do NOT invent citations.
- Multiple citations are allowed.
  Example:
  Spyware can secretly record user activity [1][3]
-When referring to a figure use:
[FIGURE:figure_id]
Example:
The architecture is shown in the network diagram
[FIGURE:a1b2c3]

Structure your answer as:
1. Simple Definition
2. Detailed Explanation
3. Real-World Example
4. Key Takeaways

USER QUESTION:
{query}


DOCUMENT CONTEXT:
{context}

AVAILABLE FIGURES:
{figure_context}


DETAILED EXPLANATION:
"""