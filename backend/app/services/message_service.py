from app.models.message import Message


def create_message(db, chat_id, role, content):
    message = Message(
        chat_id=chat_id,
        role=role,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(db, chat_id):
    return db.query(Message).filter(Message.chat_id == chat_id).all()