from app.comparison.retrieval import (
    get_document_chunks
)

from app.comparison.prompt_builder import (
    build_comparison_prompt
)

from app.llm.factory import (
    get_llm_provider
)


def compare_documents(

    db,

    workspace_id,

    subject_id,

    document_a_id,

    document_b_id,

    query,

    provider="ollama"
):

    document_a_chunks = get_document_chunks(

        db,

        document_a_id
    )

    document_b_chunks = get_document_chunks(

        db,

        document_b_id
    )

    prompt = build_comparison_prompt(

        query=query,

        document_a_chunks=document_a_chunks,

        document_b_chunks=document_b_chunks
    )

    llm = get_llm_provider(
        provider
    )

    answer = llm.generate(
        prompt
    )

    return {

        "query": query,

        "answer": answer,

        "document_a_id": document_a_id,

        "document_b_id": document_b_id,

        "sources_a": document_a_chunks[:5],

        "sources_b": document_b_chunks[:5]
    }