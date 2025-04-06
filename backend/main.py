from fastapi import FastAPI , WebSocket , WebSocketDisconnect
from app.agent import Agent

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.websocket("/ws/api/v1/generate_report")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    agent = Agent(websocket)
    try:
        await agent.agent_executor()
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")



