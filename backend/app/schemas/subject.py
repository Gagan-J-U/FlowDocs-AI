from pydantic import BaseModel
from datetime import datetime

class SubjectCreate(BaseModel):
    name: str
    workspace_id: str


class SubjectResponse(BaseModel):
    id: str
    name: str
    workspace_id: str
    created_at: datetime

    class Config:
        from_attributes = True
    