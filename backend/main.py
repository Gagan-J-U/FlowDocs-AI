from fastapi import FastAPI

from app.api.routes.workspace import router as workspace_router
from app.api.routes.subject import router as subject_router
from app.api.routes.document import router as document_router
from app.api.routes.auth import router as auth_router
from app.api.routes import chat
from app.api.routes import chat_stream

app=FastAPI()

app.include_router(workspace_router)
app.include_router(subject_router)
app.include_router(document_router)
app.include_router(auth_router)
app.include_router(chat.router)
app.include_router(chat_stream.router)

@app.get("/")
def root():
  return {"message":"Flow Docs API is up and running!"}
