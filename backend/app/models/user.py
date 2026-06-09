from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base
from app.core.id_generator import generate_uuid


class User(Base):

    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    workspaces = relationship(
        "Workspace",
        back_populates="user",
        cascade="all, delete"
    )

    workspace_memberships = relationship(
        "WorkspaceMember",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    research_profile = relationship(
        "ResearchProfile",
        uselist=False
    )

    dm_participations = relationship(
        "DMParticipant"
    )

    dm_messages = relationship(
        "DMMessage"
    )