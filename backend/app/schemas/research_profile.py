from pydantic import BaseModel
from datetime import datetime


class ResearchProfileCreate(BaseModel):

    bio: str | None = None

    institution: str | None = None

    department: str | None = None

    skills: str | None = None

    interests: str | None = None

    github_url: str | None = None

    linkedin_url: str | None = None

    website_url: str | None = None

    visibility: str = "public"


class ResearchProfileResponse(BaseModel):

    id: str

    user_id: str

    bio: str | None

    institution: str | None

    department: str | None

    skills: str | None

    interests: str | None

    github_url: str | None

    linkedin_url: str | None

    website_url: str | None

    visibility: str

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True