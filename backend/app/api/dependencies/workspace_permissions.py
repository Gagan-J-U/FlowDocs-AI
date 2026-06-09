from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember

from app.api.dependencies.auth import (
    get_current_user
)

from app.models.user import User


ROLE_HIERARCHY = {

    "viewer": 1,

    "editor": 2,

    "owner": 3
}


def require_workspace_role(
    minimum_role: str
):

    def dependency(

        workspace_id: str,

        db: Session = Depends(
            get_db
        ),

        current_user: User = Depends(
            get_current_user
        )
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

        # Workspace owner shortcut

        if workspace.user_id == current_user.id:

            return workspace

        member = (

            db.query(
                WorkspaceMember
            )

            .filter(

                WorkspaceMember.workspace_id
                == workspace_id,

                WorkspaceMember.user_id
                == current_user.id
            )

            .first()
        )

        if not member:

            raise HTTPException(

                status_code=
                status.HTTP_403_FORBIDDEN,

                detail=
                "Not a workspace member"
            )

        member_level = ROLE_HIERARCHY.get(
            member.role,
            0
        )

        required_level = ROLE_HIERARCHY.get(
            minimum_role,
            999
        )

        if member_level < required_level:

            raise HTTPException(

                status_code=
                status.HTTP_403_FORBIDDEN,

                detail=
                "Insufficient permissions"
            )

        return workspace

    return dependency