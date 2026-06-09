from fastapi import APIRouter
from fastapi import Depends

from app.models.user import User

from app.api.dependencies.auth import (
    get_current_user
)

from app.services.presence_service import (
    presence_service
)

router = APIRouter(
    prefix="/presence",
    tags=["Presence"]
)


@router.get("/{user_id}")
def get_presence(
    user_id: str,
    current_user: User = Depends(
        get_current_user
    )
):
    return {
        "user_id": user_id,
        "online": presence_service.is_online(
            user_id
        ),
        "last_seen": (
            presence_service.last_seen(
                user_id
            )
        )
    }