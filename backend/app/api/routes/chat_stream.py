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
    stream_persistent_chat_response
)
from app.api.dependencies.auth import (
    get_current_user
)
from app.models.user import User


router = APIRouter(

    prefix="/chat-stream",

    tags=["Chat Stream"]
)


@router.post("/")
def stream_chat(

    request: ChatRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    generator = stream_persistent_chat_response(

        db=db,

        user_id=current_user.id,

        workspace_id=request.workspace_id,

        subject_id=request.subject_id,

        query=request.query,

        mode=request.mode,

        provider=request.provider,

        conversation_id=request.conversation_id
    )

    return StreamingResponse(

        generator,

        media_type="text/event-stream",

        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
