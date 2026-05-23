from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base

from app.core.id_generator import (
    generate_uuid
)


class Message(Base):

    __tablename__ = "messages"

    id = Column(

        String,

        primary_key=True,

        default=generate_uuid
    )

    conversation_id = Column(

        String,

        ForeignKey("conversations.id"),

        nullable=False
    )

    sender_id = Column(

        String,

        ForeignKey("users.id"),

        nullable=True
    )

    role = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    citations = Column(
        Text,
        nullable=True
    )

    created_at = Column(

        DateTime,

        default=datetime.utcnow
    )

    # Relationships
    conversation = relationship(

        "Conversation",

        back_populates="messages"
    )