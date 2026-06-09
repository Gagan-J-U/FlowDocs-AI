from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.api.dependencies.auth import get_current_user

from app.models.subject import Subject
from app.models.user import User

from app.schemas.subject import (
    SubjectCreate,
    SubjectResponse
)

from app.services.workspace_access_service import (
    list_accessible_workspaces,
    verify_workspace_access,
)

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)


@router.post("/", response_model=SubjectResponse)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    verify_workspace_access(
        db=db,
        workspace_id=subject.workspace_id,
        user_id=current_user.id,
    )

    new_subject = Subject(
        name=subject.name,
        workspace_id=subject.workspace_id
    )

    db.add(new_subject)

    db.commit()

    db.refresh(new_subject)

    return new_subject


@router.get("/", response_model=list[SubjectResponse])
def get_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    accessible_workspaces = list_accessible_workspaces(
        db=db,
        user_id=current_user.id,
    )
    workspace_ids = [workspace.id for workspace in accessible_workspaces]

    if not workspace_ids:
        return []

    return (
        db.query(Subject)
        .filter(Subject.workspace_id.in_(workspace_ids))
        .order_by(Subject.created_at.desc())
        .all()
    )
