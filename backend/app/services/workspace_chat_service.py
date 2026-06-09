from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import status

from app.models.workspace_message import WorkspaceMessage
from app.models.workspace_member import WorkspaceMember
from app.services.workspace_access_service import verify_workspace_access
from app.services.notification_service import create_notification


def get_workspace_messages(
    db: Session,
    workspace_id: str,
    user_id: str,
):
    verify_workspace_access(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
    )

    messages = (
        db.query(WorkspaceMessage)
        .filter(WorkspaceMessage.workspace_id == workspace_id)
        .order_by(WorkspaceMessage.created_at.asc())
        .all()
    )

    return [
        {
            "id": message.id,
            "workspace_id": message.workspace_id,
            "sender_id": message.sender_id,
            "sender_username": message.sender.username if message.sender else None,
            "content": message.content,
            "created_at": message.created_at,
        }
        for message in messages
    ]


def send_workspace_message(
    db: Session,
    workspace_id: str,
    sender_id: str,
    content: str,
):
    workspace = verify_workspace_access(
        db=db,
        workspace_id=workspace_id,
        user_id=sender_id,
    )

    message = WorkspaceMessage(
        workspace_id=workspace_id,
        sender_id=sender_id,
        content=content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    result = {
        "id": message.id,
        "workspace_id": message.workspace_id,
        "sender_id": message.sender_id,
        "sender_username": message.sender.username if message.sender else None,
        "content": message.content,
        "created_at": message.created_at,
    }

    recipients = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id != sender_id,
        )
        .all()
    )

    for recipient in recipients:
        create_notification(
            db=db,
            user_id=recipient.user_id,
            type="workspace_message",
            title="New workspace message",
            message=f"New message in {workspace.name}",
        )

    return message
