from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import (
    get_db
)

from app.schemas.comparison import (
    ComparisonRequest
)

from app.chat.pipelines.comparison_pipeline import (
    ComparisonPipeline
)

router = APIRouter(

    prefix="/comparison",

    tags=["Comparison"]
)

pipeline = ComparisonPipeline()


@router.post("/")
def compare_documents(

    request: ComparisonRequest,

    db: Session = Depends(get_db)
):

    return pipeline.run(

        db=db,

        workspace_id=request.workspace_id,

        subject_id=request.subject_id,

        document_a_id=request.document_a_id,

        document_b_id=request.document_b_id,

        query=request.query,

        provider=request.provider
    )