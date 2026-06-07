import json

from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.conversation import (
    Conversation
)

from app.models.message import (
    Message
)

from app.models.subject import (
    Subject
)

from app.models.workspace import (
    Workspace
)

from app.chat.orchestrator import (
    orchestrator
)

from app.services.figure_citation_service import (
    extract_figure_ids
)


def generate_chat_response(

    db: Session,

    user_id: str,

    query: str,

    chat_type: str = "rag",

    workspace_id: str | None = None,

    subject_id: str | None = None,

    mode: str = "default",

    provider: str = "ollama",

    conversation_id: str | None = None
):

    # ==========================================
    # Validate RAG Subject Access
    # ==========================================
    if workspace_id is None:

        raise HTTPException(
            status_code=400,
            detail="workspace_id is required"
        )
    if chat_type == "rag":

        subject = (

            db.query(Subject)

            .join(
                Workspace,
                Workspace.id == Subject.workspace_id
            )

            .filter(

                Subject.id == subject_id,

                Subject.workspace_id == workspace_id,

                Workspace.user_id == user_id
            )

            .first()
        )

        if not subject:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Subject not found"
            )

    # ==========================================
    # Create / Load Conversation
    # ==========================================
    
    if conversation_id is None:

        conversation = Conversation(

            title=query[:60],

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
                Conversation.id == conversation_id
            )

            .first()
        )

        if not conversation:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Conversation not found"
            )

    # ==========================================
    # Save User Message
    # ==========================================

    user_message = Message(

        conversation_id=conversation.id,

        sender_id=user_id,

        role="user",

        content=query
    )

    db.add(user_message)

    db.commit()

    # ==========================================
    # AI Orchestration
    # ==========================================

    result = orchestrator.handle(

        chat_type=chat_type,

        db=db,

        workspace_id=workspace_id,

        subject_id=subject_id,

        query=query,

        mode=mode,

        provider=provider
    )

    answer = result["answer"]

    referenced_figure_ids = (

        extract_figure_ids(
            answer
        )
    )

    citations = result.get(
        "citations",
        []
    )

    sources = result.get(
        "sources",
        []
    )

    figures = result.get(
        "figures",
        []
    )

    referenced_figures = [

        figure

        for figure in figures

        if figure.get("figure_id")
        in referenced_figure_ids
    ]

    # ==========================================
    # Save Assistant Message
    # ==========================================

    assistant_message = Message(

        conversation_id=conversation.id,

        role="assistant",

        content=answer,

        citations=json.dumps(
            citations
        )
    )

    db.add(assistant_message)

    db.commit()

    # ==========================================
    # Return Response
    # ==========================================

    return {

        "conversation_id": conversation.id,

        "query": query,

        "answer": answer,

        "citations": citations,

        "sources": sources,

        "figures":figures,

        "referenced_figures":referenced_figures
    }
