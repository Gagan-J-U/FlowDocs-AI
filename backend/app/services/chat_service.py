import json

from sqlalchemy.orm import Session

from app.models.conversation import (
    Conversation
)

from app.models.message import (
    Message
)

from app.rag.retriever import (
    retrieve_chunks
)

from app.prompting.factory import (
    get_prompt_strategy
)

from app.llm.factory import (
    get_llm_provider
)


def generate_chat_response(

    db: Session,

    user_id: str,

    workspace_id: str,

    subject_id: str,

    query: str,

    mode: str = "default",

    provider: str = "ollama",

    conversation_id: str | None = None
):

    # ==========================================
    # Create Conversation If Needed
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

            raise Exception(
                "Conversation not found"
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
    # Retrieve Chunks
    # ==========================================

    chunks = retrieve_chunks(

        db=db,

        workspace_id=workspace_id,

        subject_id=subject_id,

        query=query,

        top_k=5
    )

    # ==========================================
    # Build Prompt
    # ==========================================

    strategy = get_prompt_strategy(
        mode
    )

    prompt = strategy.build(

        query=query,

        chunks=chunks
    )

    # ==========================================
    # Generate AI Response
    # ==========================================

    llm = get_llm_provider(
        provider
    )

    answer = llm.generate(
        prompt
    )

    # ==========================================
    # Save Assistant Message
    # ==========================================

    assistant_message = Message(

        conversation_id=conversation.id,

        role="assistant",

        content=answer,

        citations=json.dumps(chunks)
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

        "sources": chunks
    }