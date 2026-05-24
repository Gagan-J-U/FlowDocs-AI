import json
from datetime import datetime
from typing import Any

from fastapi import HTTPException
from fastapi import status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.workspace import Workspace


def _parse_citations(raw: str | None) -> list[dict[str, Any]]:
    if not raw:
        return []

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []

    if isinstance(parsed, list):
        return [
            item
            for item in parsed
            if isinstance(item, dict)
        ]

    return []


def _conversation_for_user(
    db: Session,
    conversation_id: str,
    user_id: str
) -> Conversation:
    conversation = (
        db.query(Conversation)
        .join(Workspace, Workspace.id == Conversation.workspace_id)
        .filter(
            Conversation.id == conversation_id,
            Workspace.user_id == user_id,
            Conversation.deleted_at.is_(None)
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return conversation


def list_workspace_conversations(
    db: Session,
    workspace_id: str,
    user_id: str
) -> list[dict[str, Any]]:
    workspace = (
        db.query(Workspace)
        .filter(
            Workspace.id == workspace_id,
            Workspace.user_id == user_id
        )
        .first()
    )

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    rows = (
        db.query(
            Conversation,
            func.count(Message.id).label("message_count"),
            func.max(Message.created_at).label("latest_activity")
        )
        .outerjoin(Message, Message.conversation_id == Conversation.id)
        .filter(
            Conversation.workspace_id == workspace_id,
            Conversation.deleted_at.is_(None)
        )
        .group_by(Conversation.id)
        .order_by(func.coalesce(func.max(Message.created_at), Conversation.created_at).desc())
        .all()
    )

    summaries: list[dict[str, Any]] = []

    for conversation, message_count, latest_activity in rows:
        latest_message = (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .first()
        )
        preview = latest_message.content[:180] if latest_message else None

        summaries.append({
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at,
            "latest_message_preview": preview,
            "latest_activity": latest_activity or conversation.created_at,
            "message_count": int(message_count or 0)
        })

    return summaries


def get_conversation_detail(
    db: Session,
    conversation_id: str,
    user_id: str
) -> dict[str, Any]:
    conversation = _conversation_for_user(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id
    )

    aggregate = (
        db.query(
            func.count(Message.id).label("message_count"),
            func.max(Message.created_at).label("latest_activity")
        )
        .filter(Message.conversation_id == conversation.id)
        .first()
    )

    return {
        "id": conversation.id,
        "title": conversation.title,
        "workspace_id": conversation.workspace_id,
        "subject_id": conversation.subject_id,
        "created_by": conversation.created_by,
        "created_at": conversation.created_at,
        "latest_activity": aggregate.latest_activity if aggregate else None,
        "message_count": int(aggregate.message_count or 0) if aggregate else 0
    }


def list_conversation_messages(
    db: Session,
    conversation_id: str,
    user_id: str
) -> list[dict[str, Any]]:
    conversation = _conversation_for_user(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id
    )

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc())
        .all()
    )

    return [
        {
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "citations": _parse_citations(message.citations),
            "created_at": message.created_at
        }
        for message in messages
    ]


def delete_conversation(
    db: Session,
    conversation_id: str,
    user_id: str
) -> dict[str, Any]:
    conversation = _conversation_for_user(
        db=db,
        conversation_id=conversation_id,
        user_id=user_id
    )

    conversation.deleted_at = datetime.utcnow()
    db.add(conversation)
    db.commit()

    return {
        "id": conversation.id,
        "deleted": True
    }
