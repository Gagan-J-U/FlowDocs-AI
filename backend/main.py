from fastapi import FastAPI

from app.api.workspace import router as workspace_router
from app.api.subject import router as subject_router
from app.api.document import router as document_router

app=FastAPI()

app.include_router(workspace_router)
app.include_router(subject_router)
app.include_router(document_router)

@app.get("/")
def root():
  return {"message":"Flow Docs API is up and running!"}
