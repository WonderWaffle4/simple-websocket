from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pyperclip
import markdown

from connection_manger import manager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

TEMPLATES_DIRECTORY = "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)

@app.get("/gpt", response_class=HTMLResponse)
def gpt(request: Request):
    return templates.TemplateResponse("gpt.html", {"request": request})

def parse_reponse(response):
    try:
        html = markdown.markdown(response, extensions=["fenced_code", "codehilite"])
        return html
    except:
        return response

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_name: str = "Anonymous"):
    await manager.connect(websocket, client_name)
    try:
        while True:
            data = await websocket.receive_text()
            data = parse_reponse(data)
            await manager.send_to(data, "receiver")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
