from collections import defaultdict
from typing import Any

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self) -> None:
        self.conversation_connections: dict[str, set[WebSocket]] = defaultdict(set)
        self.workspace_connections: dict[str, set[WebSocket]] = defaultdict(set)
        self._connection_users: dict[WebSocket, str] = {}
        self.notification_connections = (defaultdict(set))

    async def connect(
        self,
        websocket: WebSocket,
        room_type: str,
        room_id: str,
        user_id: str,
    ) -> None:
        self._connection_users[websocket] = user_id
        if room_type == "conversation":
            self.conversation_connections[room_id].add(websocket)
        elif room_type == "workspace":
            self.workspace_connections[room_id].add(websocket)
        elif room_type == "notification":

            self.notification_connections[
                room_id
            ].add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        user_id = self._connection_users.pop(websocket, None)
        for connections in (self.conversation_connections, self.workspace_connections):
            for room_id, sockets in list(connections.items()):
                if websocket in sockets:
                    sockets.remove(websocket)
                    if not sockets:
                        connections.pop(room_id, None)
                    break

    async def broadcast_conversation(self, conversation_id: str, data: Any) -> None:
        for connection in list(self.conversation_connections.get(conversation_id, [])):
            await connection.send_json(data)

    async def broadcast_workspace(self, workspace_id: str, data: Any) -> None:
        for connection in list(self.workspace_connections.get(workspace_id, [])):
            await connection.send_json(data)

    async def connect(
        self,
        websocket: WebSocket,
        room_type: str,
        room_id: str,
        user_id: str,
    ) -> None:

        print(
            f"[WS CONNECT]"
            f" user={user_id}"
            f" room_type={room_type}"
            f" room_id={room_id}"
        )

        self._connection_users[websocket] = user_id

        if room_type == "conversation":
            self.conversation_connections[room_id].add(websocket)

            print(
                "Conversation connections:",
                len(
                    self.conversation_connections[
                        room_id
                    ]
                )
            )

        elif room_type == "workspace":
            self.workspace_connections[room_id].add(websocket)

            print(
                "Workspace connections:",
                len(
                    self.workspace_connections[
                        room_id
                    ]
                )
            )

    async def broadcast_workspace(
        self,
        workspace_id: str,
        data
    ):

        sockets = list(
            self.workspace_connections.get(
                workspace_id,
                []
            )
        )

        print(
            "WORKSPACE:",
            workspace_id,
            "SOCKETS:",
            len(sockets)
        )

        for connection in sockets:

            print(
                "SENDING:",
                data
            )

            await connection.send_json(
                data
            )

    async def broadcast_notification(
        self,
        user_id: str,
        data
    ):

        for socket in list(
            self.notification_connections.get(
                user_id,
                []
            )
        ):

            await socket.send_json(
                data
            )

manager = ConnectionManager()

