from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.api.dependencies.auth import get_current_user

from app.models.subject import Subject
from app.models.workspace import Workspace
from app.models.user import User

from app.schemas.subject import (
    SubjectCreate,
    SubjectResponse
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
    workspace = db.query(Workspace).filter(
        Workspace.id == subject.workspace_id,
        Workspace.user_id == current_user.id
    ).first()

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
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
    return db.query(Subject).join(Workspace).filter(
        Workspace.user_id == current_user.id
    ).all()