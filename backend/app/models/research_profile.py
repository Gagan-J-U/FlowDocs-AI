from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base
from app.core.id_generator import generate_uuid


class ResearchProfile(Base):

    __tablename__ = "research_profiles"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    bio = Column(
        Text,
        nullable=True
    )

    institution = Column(
        String,
        nullable=True
    )

    department = Column(
        String,
        nullable=True
    )

    skills = Column(
        Text,
        nullable=True
    )

    interests = Column(
        Text,
        nullable=True
    )

    github_url = Column(
        String,
        nullable=True
    )

    linkedin_url = Column(
        String,
        nullable=True
    )

    website_url = Column(
        String,
        nullable=True
    )

    visibility = Column(
        String,
        default="public"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship(
        "User"
    )