from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import (
    get_db
)

from app.schemas.chat import (
    ChatRequest
)

from app.services.chat_service import (
    generate_chat_response
)

from app.api.dependencies.auth import (
    get_current_user
)

from app.models.user import User


router = APIRouter(

    prefix="/chat",

    tags=["Chat"]
)


@router.post("/")
def chat(

    request: ChatRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    return generate_chat_response(

        db=db,

        user_id=current_user.id,

        query=request.query,

        chat_type=request.chat_type,

        workspace_id=request.workspace_id,

        subject_id=request.subject_id,

        mode=request.mode,

        provider=request.provider,

        conversation_id=request.conversation_id
    )