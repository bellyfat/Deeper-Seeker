from fastapi import FastAPI , WebSocket , WebSocketDisconnect 
from app.agent import Agent
from app.utils.connection import ConnectionManager
from starlette.websockets import WebSocketState
import asyncio


app = FastAPI()

#  connection manager for websocket clients
manager = ConnectionManager()



@app.get("/")
async def root():
    return {"message": "API is running"}

# @app.websocket("/ws/api/v1/generate_report")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     agent = Agent(websocket)
#     try:
#         await agent.agent_executor()
#     except WebSocketDisconnect:
#         print("Client disconnected")
#     except Exception as e:
#         await websocket.send_text(f"Error: {str(e)}")



@app.websocket("/ws/api/v1/generate_report")
async def websocket_endpoint(websocket: WebSocket):
    client_id = websocket.query_params.get("client_id")

    if not client_id:
        await websocket.close()
        return

    await manager.connect(client_id, websocket)
    agent = Agent(websocket, client_id, manager)

    try:
        # 🔥 Run agent_executor in the background
        await asyncio.create_task(agent.agent_executor())
    except WebSocketDisconnect:
        print(f"{client_id} got disconnected")
        manager.remove(client_id)
    except Exception as e:
        if websocket.application_state == WebSocketState.CONNECTED:
            await manager.send_msg(client_id, f"Error occurred: {e}")




