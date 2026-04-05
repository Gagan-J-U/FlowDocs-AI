from sqlalchemy import Column, String
from sqlalchemy.dialects.sqlite import BLOB
import uuid

from app.db.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)