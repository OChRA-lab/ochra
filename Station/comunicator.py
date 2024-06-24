from fastapi import FastAPI, APIRouter, Request, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, Optional

class operationExecute(BaseModel):
    operation: str
    deviceName: str
    args: Optional[Dict] = None


class Comunicator:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.router = APIRouter()
        self.devices = []
        self.router.add_api_route(
            "/process_op", self.process_operation, methods=["POST"])
        self.router.add_api_route("/ping",self.ping,methods=["GET"])
        self.app.include_router(self.router)

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0")

    def ping(self,request:Request):
        clientHost = request.client.host
        print(clientHost)
        return 

    def process_operation(self, args: operationExecute):
        try:
            for i in self.devices:
                if i.name == args.deviceName:
                    return i.execute(args.operation,**args.args)
        except Exception as e:
            raise HTTPException(500,detail= str(e))
