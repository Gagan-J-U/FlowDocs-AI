from pydantic import BaseModel
from typing import Optional


class ChatCreate(BaseModel):
    subject_id: str
    title: Optional[str] = None


class ChatResponse(BaseModel):
    id: str
    subject_id: str
    title: Optional[str]

    class Config:
        from_attributes = True