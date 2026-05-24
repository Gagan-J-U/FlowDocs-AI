from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ConversationSummary(BaseModel):
    id: str
    title: str
    created_at: datetime
    latest_message_preview: str | None
    latest_activity: datetime
    message_count: int


class ConversationDetail(BaseModel):
    id: str
    title: str
    workspace_id: str
    subject_id: str
    created_by: str
    created_at: datetime
    latest_activity: datetime | None = None
    message_count: int = 0

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    citations: list[dict[str, Any]] = []
    created_at: datetime


class DeleteConversationResponse(BaseModel):
    id: str
    deleted: bool
