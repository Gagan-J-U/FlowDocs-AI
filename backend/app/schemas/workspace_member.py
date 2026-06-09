from pydantic import BaseModel
from pydantic import EmailStr

from datetime import datetime


# ==========================================
# MEMBER RESPONSE
# ==========================================

class WorkspaceMemberResponse(BaseModel):

    id: str

    workspace_id: str

    user_id: str

    username: str

    email: EmailStr

    role: str

    created_at: datetime

    class Config:

        from_attributes = True


# ==========================================
# UPDATE MEMBER ROLE
# ==========================================

class UpdateWorkspaceMemberRoleRequest(BaseModel):

    role: str