from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.api.dependencies.auth import get_current_user

from app.models.workspace import Workspace
from app.models.user import User

from app.schemas.workspace import (
  WorkspaceCreate,
  WorkspaceResponse
)

from app.services.workspace_access_service import (
    list_accessible_workspaces,
)

router=APIRouter(
  prefix="/workspaces",
  tags=["Wokspaces"]
)

@router.post("/",response_model=WorkspaceResponse)
def create_workspace(
  workspace:WorkspaceCreate,
  db:Session=Depends(get_db),
  current_user: User = Depends(get_current_user)
  ):
    new_workspace=Workspace(
        name=workspace.name,
        user_id=current_user.id
    )
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)
    return new_workspace


@router.get("/", response_model=list[WorkspaceResponse])
def get_workspaces(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return list_accessible_workspaces(
        db=db,
        user_id=current_user.id,
    )
