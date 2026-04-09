import json
from app.models.message import Message


def create_message(db, chat_id, role, content):
    # ✅ Convert dict → string before saving
    if isinstance(content, dict):
        content = json.dumps(content)

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
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    
    result = []
    for msg in messages:
        # Create a dictionary version of the message
        msg_data = {
            "id": msg.id,
            "chat_id": msg.chat_id,
            "role": msg.role,
            "content": msg.content
        }
        
        # Try to parse the JSON string back into a dict/list
        try:
            msg_data["content"] = json.loads(msg.content)
        except (json.JSONDecodeError, TypeError):
            pass  # Keep as string if it's not valid JSON
            
        result.append(msg_data)
        
    return result
