from uuid import uuid4

from datetime import datetime

from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workspace import Workspace

from app.models.workspace_member import (
    WorkspaceMember
)

from app.models.workspace_invitation import (
    WorkspaceInvitation
)

from app.services.notification_service import (
    create_notification,
)

from app.services.workspace_access_service import (
    verify_workspace_role,
)


ALLOWED_ROLES = {

    "owner",

    "editor",

    "viewer"
}


# ==========================================
# INVITE MEMBER
# ==========================================

def create_invitation(

    db: Session,

    workspace_id: str,

    inviter_id: str,

    email: str,

    role: str
):

    if role not in ALLOWED_ROLES:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invalid role"
        )

    verify_workspace_role(
        db=db,
        workspace_id=workspace_id,
        user_id=inviter_id,
        minimum_role="owner",
    )

    workspace = (
        db.query(Workspace)
        .filter(
            Workspace.id == workspace_id
        )
        .first()
    )

    existing_invite = (

        db.query(
            WorkspaceInvitation
        )

        .filter(

            WorkspaceInvitation.workspace_id
            == workspace_id,

            WorkspaceInvitation.email
            == email,

            WorkspaceInvitation.accepted_at.is_(None)
        )

        .first()
    )

    if existing_invite:

        return existing_invite

    invited_user = (

        db.query(User)

        .filter(
            User.email == email
        )

        .first()
    )

    invitation = WorkspaceInvitation(

        workspace_id=workspace_id,

        email=email,

        role=role,

        token=str(uuid4()),

        created_by=inviter_id,

        invited_user_id=(
            invited_user.id
            if invited_user
            else None
        )
    )

    db.add(invitation)

    db.commit()

    db.refresh(invitation)

    if invited_user:
        create_notification(
            db=db,
            user_id=invited_user.id,
            type="workspace_invite",
            title="Workspace invitation received",
            message=f"You have been invited to join workspace '{workspace.name}'",
        )

    return invitation


# ==========================================
# ACCEPT INVITATION
# ==========================================

def accept_invitation(

    db: Session,

    token: str,

    user_id: str
):

    invitation = (

        db.query(
            WorkspaceInvitation
        )

        .filter(
            WorkspaceInvitation.token
            == token
        )

        .first()
    )

    if not invitation:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Invitation not found"
        )

    if invitation.accepted_at:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invitation already accepted"
        )

    if invitation.expires_at < datetime.utcnow():

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invitation expired"
        )

    existing_member = (

        db.query(
            WorkspaceMember
        )

        .filter(

            WorkspaceMember.workspace_id
            == invitation.workspace_id,

            WorkspaceMember.user_id
            == user_id
        )

        .first()
    )

    if existing_member:

        return existing_member

    member = WorkspaceMember(

        workspace_id=
        invitation.workspace_id,

        user_id=user_id,

        role=invitation.role
    )

    db.add(member)

    invitation.accepted_at = (
        datetime.utcnow()
    )

    db.commit()

    db.refresh(member)

    return member


# ==========================================
# LIST MEMBERS
# ==========================================

def get_workspace_members(

    db: Session,

    workspace_id: str
):

    return (

        db.query(
            WorkspaceMember
        )

        .filter(
            WorkspaceMember.workspace_id
            == workspace_id
        )

        .all()
    )


# ==========================================
# LIST INVITATIONS
# ==========================================

def get_workspace_invitations(

    db: Session,

    workspace_id: str
):

    return (

        db.query(
            WorkspaceInvitation
        )

        .filter(
            WorkspaceInvitation.workspace_id
            == workspace_id,
            WorkspaceInvitation.accepted_at.is_(None)
        )

        .order_by(
            WorkspaceInvitation.created_at.desc()
        )

        .all()
    )


# ==========================================
# RECEIVED INVITATIONS


def get_received_invitations(

    db: Session,

    user_id: str,

    email: str
):

    return (

        db.query(
            WorkspaceInvitation
        )

        .filter(
            WorkspaceInvitation.accepted_at.is_(None),
            (
                WorkspaceInvitation.invited_user_id
                == user_id
            ) | (
                WorkspaceInvitation.email
                == email
            )
        )

        .order_by(
            WorkspaceInvitation.created_at.desc()
        )

        .all()
    )


# ==========================================
# REMOVE MEMBER
# ==========================================

def remove_workspace_member(

    db: Session,

    workspace_id: str,

    member_user_id: str,

    requester_id: str
):

    verify_workspace_role(
        db=db,
        workspace_id=workspace_id,
        user_id=requester_id,
        minimum_role="owner",
    )

    member = (

        db.query(
            WorkspaceMember
        )

        .filter(

            WorkspaceMember.workspace_id
            == workspace_id,

            WorkspaceMember.user_id
            == member_user_id
        )

        .first()
    )

    if not member:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Member not found"
        )

    db.delete(member)

    db.commit()


# ==========================================
# UPDATE ROLE
# ==========================================

def update_member_role(

    db: Session,

    workspace_id: str,

    member_user_id: str,

    role: str,

    requester_id: str
):

    if role not in ALLOWED_ROLES:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invalid role"
        )

    verify_workspace_role(
        db=db,
        workspace_id=workspace_id,
        user_id=requester_id,
        minimum_role="owner",
    )

    member = (

        db.query(
            WorkspaceMember
        )

        .filter(

            WorkspaceMember.workspace_id
            == workspace_id,

            WorkspaceMember.user_id
            == member_user_id
        )

        .first()
    )

    if not member:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Member not found"
        )

    member.role = role

    db.commit()

    db.refresh(member)

    return member