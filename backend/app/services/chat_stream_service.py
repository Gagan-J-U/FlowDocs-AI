from app.rag.retriever import (
    retrieve_chunks
)

from app.prompting.factory import (
    get_prompt_strategy
)

from app.llm.factory import (
    get_llm_provider
)


def stream_chat_response(

    db,

    workspace_id,

    subject_id,

    query,

    mode="default",

    provider="ollama"
):

    # Retrieve chunks
    chunks = retrieve_chunks(

        db=db,

        workspace_id=workspace_id,

        subject_id=subject_id,

        query=query,

        top_k=5
    )

    # Prompt strategy
    strategy = get_prompt_strategy(
        mode
    )

    prompt = strategy.build(

        query=query,

        chunks=chunks
    )

    # Provider
    llm = get_llm_provider(
        provider
    )

    # Stream tokens
    for token in llm.stream(
        prompt
    ):

        yield token