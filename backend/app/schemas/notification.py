from datetime import datetime
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    type: str
    title: str
    message: str | None = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
