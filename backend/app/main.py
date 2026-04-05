from fastapi import FastAPI
from app.db.database import Base, engine

from app.models import subject  # IMPORTANT
from app.api.routes import subject


app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

app.include_router(subject.router, prefix="/subjects", tags=["Subjects"])


@app.get("/")
def root():
    return {"message": "FlowDocs AI running"}