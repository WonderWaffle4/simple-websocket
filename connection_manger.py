from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}  # Format: {websocket: {"name": str}}

    async def connect(self, websocket: WebSocket, client_name: str):
        await websocket.accept()
        self.active_connections[websocket] = {"name": client_name}
        await self.broadcast(f"System: {client_name} joined the chat!")

    async def disconnect(self, websocket: WebSocket):
        client_info = self.active_connections.get(websocket)
        if client_info:
            print(f'Client left: {client_info["name"]}')
            del self.active_connections[websocket]

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_to(self, message: str, name: str):
        for connection, info in self.active_connections.items():
            if info["name"] == name:
                await connection.send_text(message)

manager = ConnectionManager()
