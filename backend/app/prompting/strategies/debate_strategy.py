from app.prompting.strategies.base import (
    BasePromptStrategy
)


class DebateStrategy(
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

Your goal is to teach the concept clearly, naturally, and in a beginner-friendly way using the provided document context as grounding material.

Instructions:
- Explain concepts in simple language.
- Teach step-by-step when helpful.
- Expand and clarify ideas naturally instead of copying text directly.
- Use examples, comparisons, or analogies if they improve understanding.
- Explain important technical terms when introducing them.
- Stay faithful to the provided context and avoid unsupported claims.
- Keep the explanation engaging and educational rather than overly formal.
- Avoid repeatedly mentioning the existence of documents or context.
- If the context is incomplete, clearly mention what information is missing.
- Use inline citations where appropriate using:
  [source_number]
- Use only citation numbers that exist in the context.
- Do not invent citations.
- Important factual claims should generally include citations.
- Multiple citations are allowed when combining information from multiple sources.

Example citation usage:
Spyware can secretly monitor user activity and record keystrokes [1][2].

Preferred response structure:
1. Simple Definition
2. Detailed Explanation
3. Real-World Example
4. Key Takeaways

USER QUESTION:
{query}


DOCUMENT CONTEXT:
{context}


DETAILED EXPLANATION:
"""     