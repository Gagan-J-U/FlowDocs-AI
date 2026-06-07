from pydantic import BaseModel


class ComparisonRequest(BaseModel):

    workspace_id: str

    subject_id: str

    document_a_id: str

    document_b_id: str

    query: str

    provider: str = "ollama"