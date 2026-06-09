import json

from fastapi import HTTPException
from fastapi import status

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.subject import Subject
from app.models.workspace import Workspace
from app.rag.retriever import (
    retrieve_chunks
)

from app.prompting.factory import (
    get_prompt_strategy
)

from app.llm.factory import (
    get_llm_provider
)
from app.services.citation_service import (
    build_citation_block
)

from app.services.workspace_access_service import (
    verify_workspace_access,
)
from app.rag.figure_retriever import retrieve_figures
from app.services.figure_citation_service import extract_figure_ids



def _sse(event: str, payload: dict) -> str:
    return (
        f"event: {event}\n"
        f"data: {json.dumps(payload, default=str)}\n\n"
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


def stream_persistent_chat_response(
    db,
    user_id: str,
    workspace_id: str,
    subject_id: str,
    query: str,
    mode: str = "default",
    provider: str = "ollama",
    conversation_id: str | None = None
):
    verify_workspace_access(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    subject = (
        db.query(Subject)
        .filter(
            Subject.id == subject_id,
            Subject.workspace_id == workspace_id,
        )
        .first()
    )

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    if conversation_id is None:
        conversation = Conversation(
            title=query[:60] or "Untitled conversation",
            workspace_id=workspace_id,
            subject_id=subject_id,
            created_by=user_id
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    else:
        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.created_by == user_id,
                Conversation.workspace_id == workspace_id,
                Conversation.subject_id == subject_id,
                Conversation.deleted_at.is_(None)
            )
            .first()
        )

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

    user_message = Message(
        conversation_id=conversation.id,
        sender_id=user_id,
        role="user",
        content=query
    )
    db.add(user_message)
    db.commit()

    


    chunks = retrieve_chunks(
        db=db,
        workspace_id=workspace_id,
        subject_id=subject_id,
        query=query,
        top_k=5
    )

    figures = retrieve_figures(
        db=db,
        workspace_id=workspace_id,
        subject_id=subject_id,
        query=query,
        top_k=5
    )

    citations = build_citation_block(chunks)

    strategy = get_prompt_strategy(mode)

    prompt = strategy.build(
        query=query,
        chunks=chunks,
        figures=figures
    )

    llm = get_llm_provider(provider)
    answer_parts: list[str] = []

    partial_saved = False



    def save_assistant_message() -> None:
        nonlocal partial_saved

        if partial_saved:
            return

        answer = "".join(answer_parts)
        if not answer:
            return

        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
            citations=json.dumps(citations)
        )
        db.add(assistant_message)
        db.commit()
        partial_saved = True

    try:
        for token in llm.stream(prompt):
            if not token:
                continue

            answer_parts.append(token)
            yield _sse(
                "token",
                {
                    "token": token
                }
            )
    except GeneratorExit:
        save_assistant_message()
        raise
    except Exception as exc:
        db.rollback()
        yield _sse(
            "error",
            {
                "message": str(exc)
            }
        )
        return

    save_assistant_message()

    answer = "".join(answer_parts)

    referenced_figure_ids = extract_figure_ids(
        answer
    )

    referenced_figures = [
        figure
        for figure in figures
        if figure.get("figure_id")
        in referenced_figure_ids
    ]

    save_assistant_message()

    yield _sse(
        "done",
        {
            "conversation_id": conversation.id,
            "citations": citations,
            "figures": figures,
            "referenced_figures": referenced_figures
        }
    )
