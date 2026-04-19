'''
Communicate with teh Unity backend via websockets 

*installations*
    FastAPI: https://fastapi.tiangolo.com/advanced/websockets/
    Uvicorn: https://uvicorn.dev/
        handles actual hosting to handle incoming HTTP requests 
    
communication on unity side: https://github.com/endel/NativeWebSocket


uvicorn websocket:app --reload
'''
from main_thread_new import record

from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Unity is trying to connect...")
    await websocket.accept()
    print("ACCEPTED!")
    while True:
        await websocket.send_text("i love lesbians")
        data = await websocket.receive_text()
        # Process the received data (e.g., AI inference)
        response = f"Processed: {data}"
        await websocket.send_text(response)

