from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.websocket.connection_manager import (
    manager
)

import asyncio


def list_notifications(
    db: Session,
    user_id: str,
):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def create_notification(
    db: Session,
    user_id: str,
    type: str,
    title: str,
    message: str | None = None,
):
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    

    try:

        asyncio.create_task(
            manager.broadcast_notification(
                user_id,
                {
                    "id": notification.id,
                    "type": notification.type,
                    "title": notification.title,
                    "message": notification.message,
                    "created_at": notification.created_at.isoformat()
                }
            )
        )

    except RuntimeError:
        pass
    return notification


def mark_notification_read(
    db: Session,
    notification_id: str,
    user_id: str,
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id,
        )
        .first()
    )
    if not notification:
        return None
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification
