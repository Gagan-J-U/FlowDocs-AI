from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base
from app.core.id_generator import generate_uuid
from sqlalchemy import ForeignKey


class Workspace(Base):

    __tablename__ = "workspaces"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    subjects = relationship(
        "Subject",
        back_populates="workspace",
        cascade="all, delete"
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="workspaces"
    )