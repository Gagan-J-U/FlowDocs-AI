from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.subject import SubjectCreate, SubjectResponse
from app.services.subject_service import create_subject, get_subjects
from app.api.deps import get_db

router = APIRouter()


@router.post("/", response_model=SubjectResponse)
def create_subject_route(data: SubjectCreate, db: Session = Depends(get_db)):
    return create_subject(db, data)


@router.get("/", response_model=list[SubjectResponse])
def get_subjects_route(db: Session = Depends(get_db)):
    return get_subjects(db)