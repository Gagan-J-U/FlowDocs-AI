import json
from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user_ws
from app.core.database import get_db
from app.models.user import User
from app.services.dm_service import (
    send_dm_message,
    verify_dm_access,
)
from app.services.workspace_chat_service import send_workspace_message
from app.services.workspace_access_service import verify_workspace_access
from app.services.presence_service import presence_service
from app.websocket.connection_manager import manager
from app.services.notification_service import (
    create_notification
)

from app.services.dm_service import (
    get_dm_conversation
)

router = APIRouter(
    prefix="/ws",
    tags=["Websockets"],
)


@router.websocket("/dm/{conversation_id}")
async def websocket_dm(
    conversation_id: str,
    websocket: WebSocket,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_ws),
):
    try:
        await websocket.accept()
    except Exception:
        return

    try:
        verify_dm_access(
            db=db,
            conversation_id=conversation_id,
            user_id=current_user.id,
        )
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(
        websocket=websocket,
        room_type="conversation",
        room_id=conversation_id,
        user_id=current_user.id,
    )
    presence_service.set_online(current_user.id)

    try:
        while True:
            raw = await websocket.receive_text()
            payload = json.loads(raw)
            content = payload.get("content")
            if not content or not isinstance(content, str) or not content.strip():
                await websocket.send_json({"error": "Message content cannot be empty"})
                continue

            message = send_dm_message(
                db=db,
                conversation_id=conversation_id,
                sender_id=current_user.id,
                content=content.strip(),
            )
            conversation = (
                get_dm_conversation(
                    db,
                    conversation_id
                )
            )

            for participant in conversation.participants:

                if (
                    participant.user_id
                    != current_user.id
                ):

                    create_notification(
                        db=db,
                        user_id=participant.user_id,
                        type="direct_message",
                        title=f"New message from {current_user.username}",
                        message=content[:100]
                    )
            response = {
                "id": message.id,
                "conversation_id": conversation_id,
                "sender_id": message.sender_id,
                "sender_name": message.sender.username,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            }
            await manager.broadcast_conversation(conversation_id, response)
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
        presence_service.set_offline(current_user.id)


@router.websocket("/workspaces/{workspace_id}")
async def websocket_workspace(
    workspace_id: str,
    websocket: WebSocket,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_ws),
):
    try:
        await websocket.accept()
    except Exception:
        return

    try:
        verify_workspace_access(db=db, workspace_id=workspace_id, user_id=current_user.id)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(
        websocket=websocket,
        room_type="workspace",
        room_id=workspace_id,
        user_id=current_user.id,
    )
    presence_service.set_online(current_user.id)

    try:
        while True:
            raw = await websocket.receive_text()
            payload = json.loads(raw)
            content = payload.get("content")
            if not content or not isinstance(content, str) or not content.strip():
                await websocket.send_json({"error": "Message content cannot be empty"})
                continue

            message = send_workspace_message(
                db=db,
                workspace_id=workspace_id,
                sender_id=current_user.id,
                content=content.strip(),
            )
            response = {
                "id": message.id,
                "workspace_id": workspace_id,
                "sender_id": message.sender_id,
                "sender_name": message.sender.username,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            }
            print(
                "WORKSPACE BROADCAST:",
                response
            )
            await manager.broadcast_workspace(workspace_id, response)
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
        presence_service.set_offline(current_user.id)

@router.websocket("/notifications")
async def websocket_notifications(
    websocket: WebSocket,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_ws
    ),
):

    await websocket.accept()

    await manager.connect(
        websocket=websocket,
        room_type="notification",
        room_id=current_user.id,
        user_id=current_user.id,
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )