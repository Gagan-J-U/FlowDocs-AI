from pydantic import BaseModel


class SubjectCreate(BaseModel):
    name: str


class SubjectResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True