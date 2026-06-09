from pydantic import BaseModel
from datetime import datetime


class CreateDMConversationRequest(
    BaseModel
):

    user_id: str


class DMConversationResponse(
    BaseModel
):

    id: str

    other_user_id: str

    other_username: str

    latest_message: str | None = None

    latest_message_at: datetime | None = None


class SendDMMessageRequest(
    BaseModel
):

    content: str


class DMMessageResponse(
    BaseModel
):

    id: str

    sender_id: str

    content: str

    created_at: datetime