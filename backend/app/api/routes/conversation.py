from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.conversation import (
    ConversationDetail,
    ConversationSummary,
    DeleteConversationResponse,
    MessageResponse,
)
from app.services.conversation_service import (
    delete_conversation,
    get_conversation_detail,
    list_conversation_messages,
    list_workspace_conversations,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[ConversationSummary]
)
def get_workspace_conversations(
    workspace_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return list_workspace_conversations(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetail
)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_conversation_detail(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
def get_conversation_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return list_conversation_messages(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )


@router.delete(
    "/{conversation_id}",
    response_model=DeleteConversationResponse
)
def remove_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )
