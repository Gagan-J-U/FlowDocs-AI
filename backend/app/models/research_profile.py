from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import JSON
from sqlalchemy import ForeignKey

from app.core.database import Base
from app.core.id_generator import generate_uuid


class ResearchProfile(Base):
    __tablename__ = "research_profiles"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        unique=True
    )

    full_name = Column(String)

    bio = Column(Text)

    institution = Column(String)

    research_interests = Column(JSON)

    skills = Column(JSON)