from sqlalchemy.orm import Session, selectinload
import logging

from fastapi import HTTPException
from fastapi import status

from app.models.user import User

from app.models.dm_conversation import (
    DMConversation
)

from app.models.dm_participant import (
    DMParticipant
)

from app.models.dm_message import (
    DMMessage
)
from app.services.notification_service import (
    create_notification
)
from app.services.presence_service import (
    presence_service
)



# ==========================================
# VERIFY PARTICIPANT
# ==========================================

def verify_dm_access(

    db: Session,

    conversation_id: str,

    user_id: str
):

    participant = (

        db.query(
            DMParticipant
        )

        .filter(

            DMParticipant.conversation_id
            == conversation_id,

            DMParticipant.user_id
            == user_id
        )

        .first()
    )

    if not participant:

        raise HTTPException(

            status_code=
            status.HTTP_403_FORBIDDEN,

            detail=
            "DM access denied"
        )


# ==========================================
# CREATE OR GET CONVERSATION
# ==========================================

def create_dm_conversation(

    db: Session,

    current_user_id: str,

    other_user_id: str
):

    if current_user_id == other_user_id:

        raise HTTPException(

            status_code=
            status.HTTP_400_BAD_REQUEST,

            detail=
            "Cannot message yourself"
        )

    other_user = (

        db.query(User)

        .filter(
            User.id == other_user_id
        )

        .first()
    )

    if not other_user:

        raise HTTPException(

            status_code=
            status.HTTP_404_NOT_FOUND,

            detail=
            "User not found"
        )

    existing = (

        db.query(
            DMConversation
        )

        .join(
            DMParticipant
        )

        .filter(

            DMParticipant.user_id.in_(
                [
                    current_user_id,
                    other_user_id
                ]
            )
        )

        .all()
    )

    for conversation in existing:

        participants = {

            p.user_id

            for p in conversation.participants
        }

        if participants == {

            current_user_id,

            other_user_id
        }:

            return conversation

    conversation = DMConversation()

    db.add(
        conversation
    )

    db.flush()

    db.add(

        DMParticipant(

            conversation_id=
            conversation.id,

            user_id=
            current_user_id
        )
    )

    db.add(

        DMParticipant(

            conversation_id=
            conversation.id,

            user_id=
            other_user_id
        )
    )

    db.commit()

    db.refresh(
        conversation
    )

    return conversation


# ==========================================
# GET CONVERSATION
# ==========================================

def get_dm_conversation(
    db: Session,
    conversation_id: str,
):
    conversation = (
        db.query(
            DMConversation
        )
        .filter(
            DMConversation.id == conversation_id
        )
        .first()
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DM conversation not found"
        )
    return conversation


# ==========================================
# LIST CONVERSATIONS
# ==========================================

def list_dm_conversations(
    db: Session,
    user_id: str,
) -> list[dict]:
    """Return a list of conversations for a user with eager loading to avoid N+1 queries.
    Each dict contains id, other_user_id, other_username, latest_message, latest_message_at.
    """
    logger = logging.getLogger(__name__)
    # Query conversations where the user is a participant, eager load participants and messages
    conversations = (
        db.query(DMConversation)
        .join(DMParticipant)
        .filter(DMParticipant.user_id == user_id)
        .options(
            selectinload(DMConversation.participants),
            selectinload(DMConversation.messages),
        )
        .all()
    )
    results = []
    for conversation in conversations:
        # Find the other participant
        other = next(
            (
                p.user
                for p in conversation.participants
                if p.user_id != user_id
            ),
            None,
        )
        # Get latest message if any (messages are already loaded)
        latest_message = (
            max(conversation.messages, key=lambda m: m.created_at) if conversation.messages else None
        )
        results.append(
            {
                "id": conversation.id,
                "other_user_id": other.id if other else None,
                "other_username": other.username if other else "Unknown",
                "latest_message": latest_message.content if latest_message else None,
                "latest_message_at": latest_message.created_at if latest_message else None,
                "online": (
                    presence_service.is_online(
                        other.id
                    )
                    if other
                    else False
                ),
            }
        )
    logger.debug("list_dm_conversations returned %d results for user %s", len(results), user_id)
    return results


# ==========================================
# SEND MESSAGE
# ==========================================

def send_dm_message(

    db: Session,

    conversation_id: str,

    sender_id: str,

    content: str
):

    verify_dm_access(

        db,

        conversation_id,

        sender_id
    )

    message = DMMessage(

        conversation_id=
        conversation_id,

        sender_id=
        sender_id,

        content=content
    )

    db.add(
        message
    )

    db.commit()

    db.refresh(
        message
    )
  
    participants = (
        db.query(DMParticipant)
        .filter(
            DMParticipant.conversation_id
            == conversation_id,
            DMParticipant.user_id
            != sender_id
        )
        .all()
    )

    for participant in participants:

        create_notification(
            db=db,
            user_id=participant.user_id,
            type="dm_message",
            title="New direct message",
            message=content[:120]
        )

    return message


# ==========================================
# GET MESSAGES
# ==========================================

def get_dm_messages(

    db: Session,

    conversation_id: str,

    user_id: str
):

    verify_dm_access(

        db,

        conversation_id,

        user_id
    )

    return (

        db.query(
            DMMessage
        )

        .filter(
            DMMessage.conversation_id
            == conversation_id
        )

        .order_by(
            DMMessage.created_at.asc()
        )

        .all()
    )