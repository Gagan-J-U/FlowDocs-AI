import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.workspace import router as workspace_router
from app.api.routes.subject import router as subject_router
from app.api.routes.document import router as document_router
from app.api.routes.auth import router as auth_router
from app.api.routes import chat
from app.api.routes import chat_stream
from app.api.routes.conversation import router as conversation_router
from app.api.routes import comparison
from app.api.routes.workspace_members import router as workspace_members_router
from app.api.routes import (research)
from app.api.routes import (dm)
from app.api.routes.users import router as users_router
from app.api.routes.workspace_chat import router as workspace_chat_router
from app.api.routes.notifications import router as notifications_router
from app.api.routes.websockets import router as websockets_router
from app.api.routes import presence

app=FastAPI()

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(workspace_router)
app.include_router(subject_router)
app.include_router(document_router)
app.include_router(auth_router)
app.include_router(chat.router)
app.include_router(chat_stream.router)
app.include_router(conversation_router)
app.include_router(comparison.router)
app.include_router(workspace_members_router)
app.include_router(research.router)
app.include_router(dm.router)
app.include_router(users_router)
app.include_router(workspace_chat_router)
app.include_router(notifications_router)
app.include_router(websockets_router)
app.include_router(presence.router)

@app.get("/")
def root():
  return {"message":"Flow Docs API is up and running!"}
