from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base

from app.core.id_generator import (
    generate_uuid
)


class DMConversation(Base):

    __tablename__ = "dm_conversations"

    id = Column(

        String,

        primary_key=True,

        default=generate_uuid,

        index=True
    )

    created_at = Column(

        DateTime,

        default=datetime.utcnow
    )

    updated_at = Column(

        DateTime,

        default=datetime.utcnow,

        onupdate=datetime.utcnow
    )

    participants = relationship(

        "DMParticipant",

        back_populates="conversation",

        cascade="all, delete-orphan"
    )

    messages = relationship(

        "DMMessage",

        back_populates="conversation",

        cascade="all, delete-orphan"
    )