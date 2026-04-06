from sqlalchemy import Column, String, ForeignKey, Text
import uuid

from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = Column(String, ForeignKey("chats.id"))

    role = Column(String)  # "user" or "assistant"
    content = Column(Text)