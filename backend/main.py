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

app=FastAPI()

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173"
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

app.include_router(workspace_router)
app.include_router(subject_router)
app.include_router(document_router)
app.include_router(auth_router)
app.include_router(chat.router)
app.include_router(chat_stream.router)
app.include_router(conversation_router)

@app.get("/")
def root():
  return {"message":"Flow Docs API is up and running!"}
