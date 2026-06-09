from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint


from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base
from app.core.id_generator import generate_uuid


class WorkspaceMember(Base):

    __tablename__ = "workspace_members"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    workspace_id = Column(
        String,
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    role = Column(
        String,
        nullable=False,
        default="viewer"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    workspace = relationship(
        "Workspace",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="workspace_memberships"
    )

    __table_args__ = (

        UniqueConstraint(

            "workspace_id",

            "user_id",

            name="uq_workspace_member"
        ),
    )