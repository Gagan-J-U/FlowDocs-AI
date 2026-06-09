from datetime import datetime
from pydantic import BaseModel


class CreateWorkspaceChatMessageRequest(BaseModel):
    content: str


class WorkspaceChatMessageResponse(BaseModel):
    id: str
    workspace_id: str
    sender_id: str
    sender_username: str | None = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
