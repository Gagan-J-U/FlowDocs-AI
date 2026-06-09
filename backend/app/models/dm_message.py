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


class DMMessage(Base):

    __tablename__ = "dm_messages"

    id = Column(

        String,

        primary_key=True,

        default=generate_uuid
    )

    conversation_id = Column(

        String,

        ForeignKey(
            "dm_conversations.id"
        ),

        nullable=False
    )

    sender_id = Column(

        String,

        ForeignKey(
            "users.id"
        ),

        nullable=False
    )

    content = Column(

        Text,

        nullable=False
    )

    created_at = Column(

        DateTime,

        default=datetime.utcnow
    )

    conversation = relationship(

        "DMConversation",

        back_populates="messages"
    )

    sender = relationship(
        "User"
    )