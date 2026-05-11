from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base


class Chunk(Base):

    __tablename__ = "chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id = Column(
        Integer,
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
        "Document"
    )