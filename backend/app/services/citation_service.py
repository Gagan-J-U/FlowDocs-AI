def build_citation_block(
    chunks: list
):

    citations = []

    for idx, chunk in enumerate(chunks):

        citation = {

            "id": idx + 1,

            "document_id": chunk.get(
                "document_id"
            ),

            "section_title": chunk.get(
                "section_title"
            ),

            "parent_section": chunk.get(
                "parent_section"
            ),

            "start_page": chunk.get(
                "start_page"
            ),

            "end_page": chunk.get(
                "end_page"
            ),

            "snippet": (chunk.get(
                "text"
            ) or "")[:420],

            "hybrid_score": chunk.get(
                "hybrid_score"
            )
        }

        citations.append(
            citation
        )

    return citations
