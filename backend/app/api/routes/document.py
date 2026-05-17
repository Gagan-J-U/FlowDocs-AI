import os
import uuid
import shutil

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.subject import Subject
from app.models.document import Document

from app.schemas.document import DocumentResponse


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
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Verify subject exists
    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
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

    return document