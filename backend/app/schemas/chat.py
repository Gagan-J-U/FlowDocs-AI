from pydantic import BaseModel


class ChatRequest(BaseModel):

    query: str

    chat_type: str = "rag"

    workspace_id: str | None = None

    subject_id: str | None = None

    mode: str = "default"

    provider: str = "ollama"

    conversation_id: str | None = None


class ChatResponse(BaseModel):

    conversation_id: str

    answer: str

    figures: list = []