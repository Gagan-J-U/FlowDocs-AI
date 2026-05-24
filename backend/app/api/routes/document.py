import os
import uuid
import shutil

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.api.dependencies.auth import get_current_user

from app.models.subject import Subject
from app.models.document import Document
from app.models.user import User

from app.schemas.document import DocumentResponse

from app.services.document_ingestion_service import (
    ingest_document_by_id
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_DIR = "uploads"


@router.post(
    "/upload/{subject_id}",
    response_model=DocumentResponse
)
def upload_document(
    subject_id: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Verify subject exists and belongs to the current user
    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    if subject.workspace.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload documents to this subject"
        )

    # Create subject folder
    subject_folder = os.path.join(
        UPLOAD_DIR,
        str(subject_id)
    )

    os.makedirs(
        subject_folder,
        exist_ok=True
    )

    # Generate unique filename
    file_extension = os.path.splitext(
        file.filename
    )[1]

    stored_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    # Final file path
    file_path = os.path.join(
        subject_folder,
        stored_filename
    )

    # Save actual PDF to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Create database entry
    document = Document(
        filename=file.filename,
        stored_filename=stored_filename,
        file_path=file_path,
        mime_type=file.content_type,
        file_size=os.path.getsize(file_path),
        subject_id=subject_id
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    background_tasks.add_task(

        ingest_document_by_id,

        document_id=document.id,

        workspace_id=subject.workspace_id,

        subject_id=subject.id
    )

    return document


@router.get(
    "/subject/{subject_id}",
    response_model=list[DocumentResponse]
)
def get_subject_documents(
    subject_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    if subject.workspace.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view documents for this subject"
        )

    return (
        db.query(Document)
        .filter(Document.subject_id == subject_id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )
