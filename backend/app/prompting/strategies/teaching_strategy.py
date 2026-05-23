from app.prompting.strategies.base import (
    BasePromptStrategy
)


class TeachingStrategy(
    BasePromptStrategy
):

    def build(

        self,

        query: str,

        chunks: list
    ):

        context = "\n\n".join(

            [
                chunk["text"]

                for chunk in chunks
            ]
        )

        return f"""
You are an expert educational AI tutor.

Your goal is to teach the concept clearly to a beginner using the provided context.

Instructions:
- Explain step-by-step in simple language.
- Give a detailed explanation.
- Explain technical terms when introduced.
- Use examples and analogies when useful.
- Teach naturally instead of summarizing the text.
- Use the document context as factual grounding.
- Do not mention "the provided documents" in the answer.
- If the context is insufficient, clearly state what is missing.

Structure your answer as:
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