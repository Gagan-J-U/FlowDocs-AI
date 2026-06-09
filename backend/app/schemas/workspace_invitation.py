from pydantic import BaseModel
from pydantic import EmailStr

from datetime import datetime


# ==========================================
# CREATE INVITATION
# ==========================================

class CreateWorkspaceInvitationRequest(BaseModel):

    email: EmailStr

    role: str = "viewer"


# ==========================================
# ACCEPT INVITATION
# ==========================================

class AcceptWorkspaceInvitationRequest(BaseModel):

    token: str


# ==========================================
# INVITATION RESPONSE
# ==========================================

class WorkspaceInvitationResponse(BaseModel):

    id: str

    workspace_id: str

    email: EmailStr

    role: str

    token: str

    created_at: datetime

    expires_at: datetime

    accepted_at: datetime | None = None

    class Config:

        from_attributes = True