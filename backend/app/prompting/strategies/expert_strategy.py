class ExpertStrategy:

    def build(
        self,
        query,
        chunks,
        figures=None
    ):

        context = "\n\n".join(

            chunk["text"]

            for chunk in chunks
        )

        return f"""
You are an expert-level assistant.

Requirements:

- Use precise terminology
- Provide detailed explanations
- Discuss implementation details
- Discuss limitations and tradeoffs
- Assume strong background knowledge

Question:

{query}

Context:

{context}
"""