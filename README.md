# Description

FastWAPI is a simple lightweight Websocket framework based on Starlette, which provide easy-to-use Python decorator to parse JSON incoming message.  

It's in the same spirit as _FastAPI_, where each decorator map to an HTTP path. But here, each decorator map to a Pydantic object, and each object map to a function. 

# Installation

`pip install fastwapi`
# Disclaimer

 - The module is available, but far from finished & polished, please do not use it in production.

# Roadmap 

- Add authent middleware
- Add background job to asynchrounosly send JSON to the client

# Usage 

See example/main.py for complete code.

Getting started in three steps :

#### Instanciates the framework and declare the Websocket HTTP endpoint.  

```python
import uvicorn
from fastwapi import FastWAPI, WebSocket
from pydantic import BaseModel

app = FastWAPI(endpoint="/ws")

```

#### Define Pyndantic model, for incoming and outgoing messages.

```python
class CM(BaseModel):
    counter: int

class SD(BaseModel):
    name: str
```

#### Map each Pydantic model to your function.

```python
@app.parse(CM)
async def parse_CM(websocket: WebSocket, data: CM):
    print("RECEIVED CM : ", data)
    await websocket.send_json(data.dict())

@app.parse(SD)
async def parse_SD(websocket: WebSocket, data: CM):
    print("RECEIVED SD : ", data)
    await websocket.send_json(data.dict())
```

## Launch your app

Either through command line "uvicorn main:app" or directly inside the python file :

```python
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
```
