from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.subject import Subject

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
    db: Session = Depends(get_db)
):
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
    db: Session = Depends(get_db)
):
    return db.query(Subject).all()