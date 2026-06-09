from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime
from datetime import timedelta

from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.id_generator import generate_uuid


class WorkspaceInvitation(Base):

    __tablename__ = "workspace_invitations"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    workspace_id = Column(
        String,
        ForeignKey("workspaces.id"),
        nullable=False
    )

    email = Column(
        String,
        nullable=False,
        index=True
    )

    role = Column(
        String,
        nullable=False,
        default="viewer"
    )

    token = Column(
        String,
        nullable=False,
        unique=True
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

    expires_at = Column(
        DateTime,
        default=lambda:
        datetime.utcnow()
        + timedelta(days=7)
    )

    accepted_at = Column(
        DateTime,
        nullable=True
    )

    workspace = relationship(
        "Workspace"
    )

    invited_user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=True
    )