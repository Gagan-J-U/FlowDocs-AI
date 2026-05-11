from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def chunk_sections(sections):

    final_chunks = []

    chunk_index = 0

    for section in sections:

        section_chunks = text_splitter.split_text(
            section["content"]
        )

        for chunk_text in section_chunks:

            final_chunks.append({

                "chunk_index": chunk_index,

                "text": chunk_text,

                "section_title": section[
                    "title"
                ],

                "parent_section": section[
                    "parent_title"
                ],

                "hierarchy_level": section[
                    "level"
                ],

                "start_page": section[
                    "start_page"
                ],

                "end_page": section[
                    "end_page"
                ]
            })

            chunk_index += 1

    return final_chunks