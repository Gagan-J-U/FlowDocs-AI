from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import create_message, get_messages
from app.api.deps import get_db

router = APIRouter()


@router.get("/{chat_id}", response_model=list[MessageResponse])
def get_messages_route(chat_id: str, db: Session = Depends(get_db)):
    return get_messages(db, chat_id)