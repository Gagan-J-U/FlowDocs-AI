from fastapi import APIRouter
from fastapi import Depends

from fastapi.responses import (
    StreamingResponse
)

from sqlalchemy.orm import Session

from app.core.database import (
    get_db
)

from app.schemas.chat import (
    ChatRequest
)

from app.services.chat_stream_service import (
    stream_chat_response
)


router = APIRouter(

    prefix="/chat-stream",

    tags=["Chat Stream"]
)


@router.post("/")
def stream_chat(

    request: ChatRequest,

    db: Session = Depends(get_db)
):

    generator = stream_chat_response(

        db=db,

        workspace_id=request.workspace_id,

        subject_id=request.subject_id,

        query=request.query,

        mode=request.mode,

        provider=request.provider
    )

    return StreamingResponse(

        generator,

        media_type="text/plain"
    )