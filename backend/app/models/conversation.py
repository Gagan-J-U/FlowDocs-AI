from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base

from app.core.id_generator import (
    generate_uuid
)


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(

        String,

        primary_key=True,

        default=generate_uuid
    )

    title = Column(
        String,
        nullable=False
    )

    workspace_id = Column(

        String,

        ForeignKey("workspaces.id"),

        nullable=False
    )

    subject_id = Column(

        String,

        ForeignKey("subjects.id"),

        nullable=False
    )

    created_by = Column(

        String,

        ForeignKey("users.id"),

        nullable=False
    )

    created_at = Column(

        DateTime,

        default=datetime.utcnow
    )

    deleted_at = Column(

        DateTime,

        nullable=True
    )

    is_shared = Column(
        Boolean,
        default=False,
        nullable=False
    )

    # Relationships
    messages = relationship(

        "Message",

        back_populates="conversation",

        cascade="all, delete-orphan"
    )
