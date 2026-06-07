class IntermediateStrategy:

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
You are an educational assistant.

Explain the answer for someone who already understands
basic concepts in the field.

Requirements:

- Moderate technical depth
- Clear explanations
- Include examples
- Explain important terminology

Question:

{query}

Context:

{context}
"""