from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base
from app.core.id_generator import generate_uuid


class Subject(Base):

    __tablename__ = "subjects"

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

    workspace_id = Column(
        String,
        ForeignKey("workspaces.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    workspace = relationship(
        "Workspace",
        back_populates="subjects"
    )

    documents = relationship(
        "Document",
        back_populates="subject",
        cascade="all, delete"
    )