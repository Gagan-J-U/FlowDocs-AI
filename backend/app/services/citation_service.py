def build_citation_block(
    chunks: list
):

    citations = []

    for idx, chunk in enumerate(chunks):

        citation = {

            "id": idx + 1,

            "section_title": chunk.get(
                "section_title"
            ),

            "start_page": chunk.get(
                "start_page"
            ),

            "end_page": chunk.get(
                "end_page"
            )
        }

        citations.append(
            citation
        )

    return citations