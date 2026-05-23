from pydantic import BaseModel


class ChatRequest(BaseModel):

    workspace_id: str

    subject_id: str

    query: str

    mode: str = "default"

    provider: str = "ollama"

    conversation_id: str | None = None


class ChatResponse(BaseModel):

    conversation_id: str

    answer: str