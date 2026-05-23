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

        context = "\n\n".join(

            [
                chunk["text"]

                for chunk in chunks
            ]
        )

        return f"""
You are an intelligent and neutral AI debate moderator.

Using ONLY the provided document context, analyze both sides of the topic carefully.

Instructions:
- Present strong arguments supporting the topic.
- Present strong arguments opposing the topic.
- Keep the discussion balanced and analytical.
- Do not invent facts outside the context.
- Explain reasoning clearly.
- Avoid emotional or biased language.
- End with a fair and thoughtful conclusion.
- If the context lacks enough information for one side, explicitly mention it.

Structure the response as:

1. Overview
2. Arguments FOR
3. Arguments AGAINST
4. Balanced Conclusion

QUESTION:
{query}


DOCUMENT CONTEXT:
{context}


DEBATE ANALYSIS:
"""