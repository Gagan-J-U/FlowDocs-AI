from app.prompting.strategies.base import (
    BasePromptStrategy
)


class DebateStrategy(
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
You are an expert debate moderator and analyst.

Your task is to examine the user's question from multiple perspectives using ONLY the provided document context.

Instructions:

- Construct the strongest possible argument supporting one viewpoint.
- Construct the strongest possible argument supporting an opposing viewpoint.
- Ground all arguments in the provided evidence.
- Use citations for factual claims.
- Challenge assumptions where appropriate.
- Highlight trade-offs, limitations, and risks.
- Do not invent information not present in the context.
- If the context is insufficient, explicitly state the missing information.

Citation Rules:

- Use inline citations:
  [1]
  [2]
  [1][3]

- Use only citations that exist in the provided context.
- Important factual claims should include citations.

Response Structure:

# Question

Restate the question briefly.

# Position A

Present the strongest argument supporting one side.

# Evidence Supporting Position A

Support the argument using document evidence and citations.

# Position B

Present the strongest argument supporting an alternative or opposing side.

# Evidence Supporting Position B

Support the argument using document evidence and citations.

# Rebuttal of Position A

Identify weaknesses, assumptions, risks, or limitations.

# Rebuttal of Position B

Identify weaknesses, assumptions, risks, or limitations.

# Trade-Off Analysis

Compare the benefits and drawbacks of both positions.

# Balanced Conclusion

Provide a final evidence-based conclusion.

When referring to a figure use:

[FIGURE:figure_id]

Example:

The architecture is shown in the network diagram
[FIGURE:a1b2c3]

USER QUESTION:

{query}

DOCUMENT CONTEXT:

{context}

AVAILABLE FIGURES:

{figure_context}

DEBATE ANALYSIS:
"""