from app.models.chat import Chat


def create_chat(db, data):
    chat = Chat(
        subject_id=data.subject_id,
        title=data.title
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chats_by_subject(db, subject_id):
    return db.query(Chat).filter(Chat.subject_id == subject_id).all()