from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base
from app.core.id_generator import (
    generate_uuid
)


class Figure(Base):

    __tablename__ = "figures"

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

    page_number = Column(
        Integer,
        nullable=False
    )

    figure_index = Column(
        Integer,
        nullable=False
    )

    image_filename = Column(
        String,
        nullable=False
    )

    image_path = Column(
        Text,
        nullable=False
    )

    width = Column(
        Integer,
        nullable=True
    )

    height = Column(
        Integer,
        nullable=True
    )

    caption = Column(
        Text,
        nullable=True
    )

    nearby_text = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    document = relationship(
        "Document",
        back_populates="figures"
    )