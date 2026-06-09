from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.workspace_chat import (
    CreateWorkspaceChatMessageRequest,
    WorkspaceChatMessageResponse,
)
from app.services.workspace_chat_service import (
    get_workspace_messages,
    send_workspace_message,
)

router = APIRouter(
    prefix="/workspaces/{workspace_id}/chat",
    tags=["Workspace Chat"],
)


@router.get("", response_model=list[WorkspaceChatMessageResponse])
def list_workspace_chat(
    workspace_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_workspace_messages(
        db=db,
        workspace_id=workspace_id,
        user_id=current_user.id,
    )


@router.post("", response_model=WorkspaceChatMessageResponse)
def post_workspace_chat(
    workspace_id: str,
    payload: CreateWorkspaceChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    return send_workspace_message(
        db=db,
        workspace_id=workspace_id,
        sender_id=current_user.id,
        content=payload.content.strip(),
    )
