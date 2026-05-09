from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def root():
  return {"message":"Flow Docs API is up and running!"}
