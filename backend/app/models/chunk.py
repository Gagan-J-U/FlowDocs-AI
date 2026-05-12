from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base
from app.core.id_generator import generate_uuid


class Chunk(Base):

    __tablename__ = "chunks"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    document_id = Column(
        String,
        ForeignKey("documents.id"),
        nullable=False
    )

    chunk_index = Column(
        Integer,
        nullable=False
    )

    text = Column(
        Text,
        nullable=False
    )

    section_title = Column(
        String,
        nullable=True
    )

    parent_section = Column(
        String,
        nullable=True
    )

    hierarchy_level = Column(
        Integer,
        nullable=True
    )

    start_page = Column(
        Integer,
        nullable=True
    )

    end_page = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )