from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.schemas.chat import ChatCreate, ChatResponse
from app.schemas.message import MessageCreate

from app.services.chat_service import create_chat, get_chats_by_subject
from app.services.message_service import create_message, get_messages
from app.services.rag_service import generate_rag_response

from app.models.chat import Chat
from app.models.subject import Subject

router = APIRouter()


# ✅ 1. CREATE CHAT
@router.post("/", response_model=ChatResponse)
def create_chat_route(data: ChatCreate, db: Session = Depends(get_db)):

    # Validate subject
    subject = db.query(Subject).filter(Subject.id == data.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return create_chat(db, data)


# ✅ 2. GET CHATS BY SUBJECT
@router.get("/subject/{subject_id}", response_model=list[ChatResponse])
def get_chats(subject_id: str, db: Session = Depends(get_db)):

    # Optional validation
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return get_chats_by_subject(db, subject_id)


# ✅ 3. GET SINGLE CHAT
@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: str, db: Session = Depends(get_db)):

    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat


# ✅ 4. SEND MESSAGE (RAG FLOW)
@router.post("/{chat_id}/message")
def chat(chat_id: str, data: MessageCreate, db: Session = Depends(get_db)):

    # 🔹 Validate chat
    chat_obj = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat_obj:
        raise HTTPException(status_code=404, detail="Chat not found")

    subject_id = chat_obj.subject_id

    # 🔹 Save user message
    user_msg = create_message(db, chat_id, "user", data.content)

    # 🔹 Get chat history (for better responses)
    messages = get_messages(db, chat_id)
    history = [m.content for m in messages]

    try:
        # 🔹 Generate AI response using RAG
        ai_response = generate_rag_response(
            subject_id=subject_id,
            query=data.content,
            history=history
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 🔹 Save AI message
    ai_msg = create_message(db, chat_id, "assistant", ai_response)

    return {
        "user_message": user_msg.content,
        "ai_message": ai_msg.content
    }