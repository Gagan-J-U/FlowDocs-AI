from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import (
    get_db
)

from app.api.dependencies.auth import (
    get_current_user
)

from app.models.user import (
    User
)

from app.schemas.dm import (
    CreateDMConversationRequest,
    DMConversationResponse,
    DMMessageResponse,
    SendDMMessageRequest
)

from app.services.dm_service import (
    create_dm_conversation,
    list_dm_conversations,
    get_dm_messages,
    send_dm_message
)


router = APIRouter(

    prefix="/dm",

    tags=["Direct Messages"]
)


# ==========================================
# CREATE CONVERSATION
# ==========================================

@router.post(
    "/conversations",
    response_model=DMConversationResponse,
)
def create_conversation(
    payload: CreateDMConversationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    conversation = create_dm_conversation(
        db=db,
        current_user_id=current_user.id,
        other_user_id=payload.user_id,
    )

    other_user = next(
        (
            participant.user
            for participant in conversation.participants
            if participant.user_id != current_user.id
        ),
        None,
    )

    latest_message = (
        max(
            conversation.messages,
            key=lambda message: message.created_at,
        )
        if conversation.messages
        else None
    )

    return {
        "id": conversation.id,
        "other_user_id": other_user.id if other_user else "",
        "other_username": other_user.username if other_user else "Unknown",
        "latest_message": (
            latest_message.content
            if latest_message
            else None
        ),
        "latest_message_at": (
            latest_message.created_at
            if latest_message
            else None
        ),
    }
# ==========================================
# LIST CONVERSATIONS
# ==========================================

@router.get("/conversations", response_model=list[DMConversationResponse])
def get_conversations(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return list_dm_conversations(

        db=db,

        user_id=current_user.id
    )


# ==========================================
# GET MESSAGES
# ==========================================

@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[DMMessageResponse],
)
def get_messages(

    conversation_id: str,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return get_dm_messages(

        db=db,

        conversation_id=
        conversation_id,

        user_id=
        current_user.id
    )


# ==========================================
# SEND MESSAGE
# ==========================================

@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=DMMessageResponse,
)
def send_message(

    conversation_id: str,

    payload: SendDMMessageRequest,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return send_dm_message(

        db=db,

        conversation_id=
        conversation_id,

        sender_id=
        current_user.id,

        content=
        payload.content
    )