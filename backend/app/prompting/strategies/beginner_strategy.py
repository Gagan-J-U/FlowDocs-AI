class BeginnerStrategy:

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

Explain the answer as if the user is completely new to the topic.

Requirements:

- Use simple language
- Avoid technical jargon
- Use analogies where useful
- Use real-world examples
- Explain concepts step-by-step

Question:

{query}

Context:

{context}
"""