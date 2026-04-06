from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: str
    subject_id: str
    filename: str

    class Config:
        from_attributes = True