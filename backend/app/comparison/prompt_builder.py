def build_comparison_prompt(

    query: str,

    document_a_chunks: list,

    document_b_chunks: list
):

    document_a_text = "\n\n".join(

        chunk.text

        for chunk in document_a_chunks[:10]
    )

    document_b_text = "\n\n".join(

        chunk.text

        for chunk in document_b_chunks[:10]
    )

    return f"""
You are a document comparison assistant.

Compare the two documents using ONLY
the provided context.

Question:
{query}

DOCUMENT A:

{document_a_text}

DOCUMENT B:

{document_b_text}

Provide:

1. Similarities
2. Differences
3. Important Insights
4. Final Summary

Use clear headings.
"""