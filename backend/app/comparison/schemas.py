from pydantic import BaseModel


class DocumentComparisonRequest(BaseModel):

    workspace_id: str

    subject_id: str

    document_a_id: str

    document_b_id: str

    query: str


class DocumentComparisonResponse(BaseModel):

    query: str

    answer: str

    document_a_id: str

    document_b_id: str

    sources_a: list

    sources_b: list