import json
from fastapi import WebSocket
from typing import  Any

async def send_event(websocket: WebSocket , event_type:str , data : Any) -> dict[str , Any]:
    """stream intermediate steps of agent execution as events"""
    message = {
        "event_type" : event_type,
        "event_data" : data
    }

    await websocket.send_text(json.dumps(message))
