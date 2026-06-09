from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base

from app.core.id_generator import (
    generate_uuid
)


class DMParticipant(Base):

    __tablename__ = "dm_participants"

    __table_args__ = (

        UniqueConstraint(

            "conversation_id",

            "user_id",

            name="uq_dm_participant"
        ),
    )

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

    user_id = Column(

        String,

        ForeignKey(
            "users.id"
        ),

        nullable=False
    )

    joined_at = Column(

        DateTime,

        default=datetime.utcnow
    )

    conversation = relationship(

        "DMConversation",

        back_populates="participants"
    )

    user = relationship(
        "User"
    )