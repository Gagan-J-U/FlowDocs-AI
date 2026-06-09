from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import (
    get_db
)

from app.models.user import User

from app.api.dependencies.auth import (
    get_current_user
)

from app.api.dependencies.workspace_permissions import (
    require_workspace_role
)

from app.schemas.workspace_invitation import (
    CreateWorkspaceInvitationRequest,

    AcceptWorkspaceInvitationRequest,

    WorkspaceInvitationResponse
)

from app.schemas.workspace_member import (
    UpdateWorkspaceMemberRoleRequest
)

from app.services.workspace_member_service import (
    create_invitation,

    accept_invitation,

    get_workspace_members,

    get_workspace_invitations,

    get_received_invitations,

    remove_workspace_member,

    update_member_role
)


router = APIRouter(

    prefix="/workspace-members",

    tags=["Workspace Members"]
)


# ==========================================
# INVITE USER
# ==========================================

@router.post(
    "/{workspace_id}/invite"
)
def invite_member(

    workspace_id: str,

    request:
    CreateWorkspaceInvitationRequest,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    ),

    _workspace = Depends(
        require_workspace_role(
            "owner"
        )
    )
):

    return create_invitation(

        db=db,

        workspace_id=workspace_id,

        inviter_id=current_user.id,

        email=request.email,

        role=request.role
    )


# ==========================================
# ACCEPT INVITE
# ==========================================

@router.post(
    "/accept"
)
def accept_workspace_invitation(

    request:
    AcceptWorkspaceInvitationRequest,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    return accept_invitation(

        db=db,

        token=request.token,

        user_id=current_user.id
    )


# ==========================================
# LIST MEMBERS
# ==========================================

@router.get(
    "/{workspace_id}/members"
)
def list_members(

    workspace_id: str,

    db: Session = Depends(
        get_db
    ),

    _workspace = Depends(
        require_workspace_role(
            "viewer"
        )
    )
):

    return get_workspace_members(

        db=db,

        workspace_id=workspace_id
    )


# ==========================================
# LIST INVITATIONS
# ==========================================

@router.get(
    "/{workspace_id}/invitations",
    response_model=list[WorkspaceInvitationResponse]
)
def list_invitations(

    workspace_id: str,

    db: Session = Depends(
        get_db
    ),

    _workspace = Depends(
        require_workspace_role(
            "viewer"
        )
    )
):

    return get_workspace_invitations(

        db=db,

        workspace_id=workspace_id
    )


@router.get(
    "/invitations/received",
    response_model=list[WorkspaceInvitationResponse]
)
def list_received_invitations(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )
):

    invitations = get_received_invitations(

        db=db,

        user_id=current_user.id,

        email=current_user.email
    )

    return [
        {
            "id": invite.id,
            "workspace_id": invite.workspace_id,
            "workspace_name": invite.workspace.name if invite.workspace else None,
            "email": invite.email,
            "role": invite.role,
            "token": invite.token,
            "created_at": invite.created_at,
            "expires_at": invite.expires_at,
            "accepted_at": invite.accepted_at,
        }
        for invite in invitations
    ]


# ==========================================
# REMOVE MEMBER
# ==========================================

@router.delete(
    "/{workspace_id}/members/{user_id}"
)
def delete_member(

    workspace_id: str,

    user_id: str,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    ),

    _workspace = Depends(
        require_workspace_role(
            "owner"
        )
    )
):

    remove_workspace_member(

        db=db,

        workspace_id=workspace_id,

        member_user_id=user_id,

        requester_id=current_user.id
    )

    return {

        "message":
        "Member removed"
    }


# ==========================================
# UPDATE ROLE
# ==========================================

@router.put(
    "/{workspace_id}/members/{user_id}/role"
)
def change_role(

    workspace_id: str,

    user_id: str,

    request:
    UpdateWorkspaceMemberRoleRequest,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    ),

    _workspace = Depends(
        require_workspace_role(
            "owner"
        )
    )
):

    return update_member_role(

        db=db,

        workspace_id=workspace_id,

        member_user_id=user_id,

        role=request.role,

        requester_id=current_user.id
    )