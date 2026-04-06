from sqlalchemy import Column, String, ForeignKey
import uuid
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = Column(String, ForeignKey("subjects.id"))
    filename = Column(String)
    file_path = Column(String)