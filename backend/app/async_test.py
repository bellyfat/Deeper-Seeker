import asyncio
import websockets

# Change this to match your running backend port if needed
BASE_URL = "ws://localhost:8000/ws/api/v1/generate_report"

async def test_client(client_id):
    uri = f"{BASE_URL}?client_id={client_id}"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"[Client {client_id}] Connected")

            # Send a message (you can customize this)
            await websocket.send(f"Hello from client {client_id}")
            
            # Wait for a response
            response = await websocket.recv()
            print(f"[Client {client_id}] Received: {response}")

    except websockets.exceptions.InvalidStatusCode as e:
        print(f"[Client {client_id}] Error: server rejected WebSocket connection: HTTP {e.status_code}")
    except Exception as e:
        print(f"[Client {client_id}] Unexpected error: {e}")

async def main():
    clients = [test_client(i) for i in range(1, 6)]  # Simulate 5 clients
    await asyncio.gather(*clients)

if __name__ == "__main__":
    asyncio.run(main())
