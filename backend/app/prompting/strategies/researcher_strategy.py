class ResearcherStrategy:

    def build(
        self,
        query,
        chunks,
        Figures=None
    ):

        context = "\n\n".join(

            chunk["text"]

            for chunk in chunks
        )

        return f"""
You are assisting a researcher.

Requirements:

- Use academic language
- Discuss assumptions
- Discuss implications
- Highlight limitations
- Mention open problems where relevant
- Focus on critical analysis

Question:

{query}

Context:

{context}
"""