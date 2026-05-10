from pydantic import BaseModel
from datetime import datetime

class SubjectCreate(BaseModel):
  name:str 
  workspace_id:int 

class SubjectResponse(BaseModel):
  id:int 
  name:str 
  workspace_id:int 
  created_at:datetime

  class config:
    from_attributes=True
    