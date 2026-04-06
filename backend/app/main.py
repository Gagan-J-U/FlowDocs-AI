from fastapi import FastAPI
from app.db.database import Base, engine

# models (for DB)
from app.models import subject, chat, message

# routes (rename to avoid conflict)
from app.api.routes import subject as subject_routes
from app.api.routes import chat as chat_routes
from app.api.routes import message as message_routes


app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# register routes
app.include_router(subject_routes.router, prefix="/subjects", tags=["Subjects"])
app.include_router(chat_routes.router, prefix="/chats", tags=["Chats"])
app.include_router(message_routes.router, prefix="/messages", tags=["Messages"])


@app.get("/")
def root():
    return {"message": "FlowDocs AI running"}

@app.get("/")
def root():
    return {"message": "FlowDocs AI running"}