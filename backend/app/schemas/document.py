from pydantic import BaseModel

from datetime import datetime


class DocumentResponse(BaseModel):

    id: str

    filename: str

    stored_filename: str

    file_path: str

    mime_type: str | None

    file_size: int | None

    subject_id: str

    uploaded_at: datetime

    processing_status: str | None = None

    class Config:

        from_attributes = True