from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os

from app.api.deps import get_db
from app.services.document_service import process_document
from app.models.document import Document

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/{subject_id}")
def upload_document(subject_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save in DB
    doc = Document(
        subject_id=subject_id,
        filename=file.filename,
        file_path=file_path
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # 🔥 Process document (RAG pipeline start)
    process_document(subject_id, doc.id, file_path)

    return {"message": "Uploaded & processing started"}