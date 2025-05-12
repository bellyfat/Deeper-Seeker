from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
from starlette.websockets import WebSocketState


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"[{client_id}] Connected")

    def remove(self, client_id: str):
        self.active_connections.pop(client_id, None)
        print(f"[{client_id}] Removed from active connections")

    async def send_msg(self, client_id: str, msg: str):
        websocket = self.active_connections.get(client_id)
        try:
            if websocket and websocket.application_state == WebSocketState.CONNECTED:
                await websocket.send_text(msg)
            else:
                print(f"[{client_id}] WebSocket not connected.")
        except Exception as e:
            print(f"[{client_id}] Failed to send message: {e}")

    async def broadcast(self, message: str):
        for client_id, websocket in self.active_connections.items():
            try:
                if websocket.application_state == WebSocketState.CONNECTED:
                    await websocket.send_text(message)
            except Exception as e:
                print(f"[{client_id}] Broadcast failed: {e}")
