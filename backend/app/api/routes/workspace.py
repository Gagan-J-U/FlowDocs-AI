from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db 

from app.models.workspace import Workspace

from app.schemas.workspace import (
  WorkspaceCreate,
  WorkspaceResponse
)

router=APIRouter(
  prefix="/workspaces",
  tags=["Wokspaces"]
)

@router.post("/",response_model=WorkspaceResponse)
def create_workspace(
  workspace:WorkspaceCreate,
  db:Session=Depends(get_db)
  ):
    new_workspace=Workspace(name=workspace.name)
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)
    return new_workspace


@router.get("/", response_model=list[WorkspaceResponse])
def get_workspaces(
    db: Session = Depends(get_db)
):
    return db.query(Workspace).all()