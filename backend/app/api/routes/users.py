from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import search_users as search_users_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/search",
    response_model=list[UserResponse],
)
def search_users(
    q: str = Query(..., alias="q", min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return search_users_service(
        db=db,
        current_user_id=current_user.id,
        query=q,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

