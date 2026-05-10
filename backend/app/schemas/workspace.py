from pydantic import BaseModel
from datetime import datetime

class WorkspaceCreate(BaseModel):
  name:str

class WorkspaceResponse(BaseModel):
  id:int 
  name:str 
  created_at:datetime 

  class Config:
    from_attributes=True
    