from sqlalchemy import Column, String, ForeignKey
import uuid

from app.db.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = Column(String, ForeignKey("subjects.id"))
    title = Column(String, nullable=True)