from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    role: str
    content: str

    class Config:
        from_attributes = True