from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base
from app.core.id_generator import generate_uuid


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )

    stored_filename = Column(
        String,
        nullable=False
    )

    file_path = Column(
        String,
        nullable=False
    )

    mime_type = Column(
        String,
        nullable=True
    )

    file_size = Column(
        Integer,
        nullable=True
    )

    subject_id = Column(
        String,
        ForeignKey("subjects.id"),
        nullable=False
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    subject = relationship(
        "Subject",
        back_populates="documents"
    )

    chunks = relationship(
        "Chunk",
        back_populates="document",
        cascade="all, delete"
    )