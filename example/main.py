import uvicorn
from fastwapi import FastWAPI, WebSocket
from pydantic import BaseModel

app = FastWAPI(endpoint="/ws")

class CM(BaseModel):
    counter: int

class SD(BaseModel):
    name: str

@app.parse(CM)
async def parse_CM(websocket: WebSocket, data: CM):
    print("RECEIVED CM : ", data)
    await websocket.send_json(data.dict())

@app.parse(SD)
async def parse_SD(websocket: WebSocket, data: CM):
    print("RECEIVED SD : ", data)
    await websocket.send_json(data.dict())




if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")