from fastapi import HTTPException
from fastapi import status

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.workspace import (
    Workspace
)

from app.models.workspace_member import (
    WorkspaceMember
)


ROLE_HIERARCHY = {

    "viewer": 1,

    "editor": 2,

    "owner": 3
}


# ==========================================
# WORKSPACE ACCESS
# ==========================================

def verify_workspace_access(

    db: Session,

    workspace_id: str,

    user_id: str
):

    workspace = (

        db.query(Workspace)

        .filter(
            Workspace.id == workspace_id
        )

        .first()
    )

    if not workspace:

        raise HTTPException(

            status_code=
            status.HTTP_404_NOT_FOUND,

            detail="Workspace not found"
        )

    # Workspace owner

    if workspace.user_id == user_id:

        return workspace

    member = (

        db.query(
            WorkspaceMember
        )

        .filter(

            WorkspaceMember.workspace_id
            == workspace_id,

            WorkspaceMember.user_id
            == user_id
        )

        .first()
    )

    if not member:

        raise HTTPException(

            status_code=
            status.HTTP_403_FORBIDDEN,

            detail=
            "Workspace access denied"
        )

    return workspace


def list_accessible_workspaces(
    db: Session,
    user_id: str,
):
    member_workspace_ids = (
        db.query(WorkspaceMember.workspace_id)
        .filter(WorkspaceMember.user_id == user_id)
        .subquery()
    )

    return (
        db.query(Workspace)
        .filter(
            or_(
                Workspace.user_id == user_id,
                Workspace.id.in_(member_workspace_ids),
            )
        )
        .order_by(Workspace.created_at.desc())
        .all()
    )


# ==========================================
# ROLE CHECK
# ==========================================

def verify_workspace_role(

    db: Session,

    workspace_id: str,

    user_id: str,

    minimum_role: str
):

    workspace = verify_workspace_access(

        db=db,

        workspace_id=workspace_id,

        user_id=user_id
    )

    if workspace.user_id == user_id:

        return workspace

    member = (

        db.query(
            WorkspaceMember
        )

        .filter(

            WorkspaceMember.workspace_id
            == workspace_id,

            WorkspaceMember.user_id
            == user_id
        )

        .first()
    )

    current_level = ROLE_HIERARCHY.get(

        member.role,

        0
    )

    required_level = ROLE_HIERARCHY.get(

        minimum_role,

        999
    )

    if current_level < required_level:

        raise HTTPException(

            status_code=
            status.HTTP_403_FORBIDDEN,

            detail=
            "Insufficient permissions"
        )

    return workspace