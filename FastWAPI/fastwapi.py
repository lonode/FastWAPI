from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket
from pydantic import BaseModel

class WSEndpoint(WebSocketEndpoint):
    encoding = 'json'
    
    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_receive(self, websocket, data):
        try:
            decoded, func = WAPI.decode_incoming(data)
        except:
            await websocket.send_json({"error":"invalid JSON"})
            return -1
        
        await func(websocket, decoded)

    async def on_disconnect(self, websocket, close_code):
        pass

class FastWAPI(Starlette):

    mapping_class = {}


    def decode_incoming(data: dict):
        for model in WAPI.mapping_class:
            try:
                decoded = model(**data)
                return decoded, WAPI.mapping_class[model]
            except:
                print("error")


    def __init__(self,endpoint: str):
        super().__init__(routes=[WebSocketRoute(endpoint, WSEndpoint)])
    
    def parse(self, incoming_model: BaseModel):
        def Inner(func):
            self.mapping_class[incoming_model] = func
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
            return wrapper
        return Inner