from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Original filename uploaded by user
    filename = Column(
        String,
        nullable=False
    )

    # Internal unique filename used for storage
    stored_filename = Column(
        String,
        nullable=False,
        unique=True
    )

    # Physical file location on disk
    file_path = Column(
        String,
        nullable=False
    )

    # MIME type (example: application/pdf)
    mime_type = Column(
        String,
        nullable=True
    )

    # File size in bytes
    file_size = Column(
        Integer,
        nullable=True
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    subject = relationship(
        "Subject"
    )