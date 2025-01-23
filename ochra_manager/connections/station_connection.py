from ochra_common.connections.rest_adapter import RestAdapter
from ochra_common.equipment.operation import Operation
import logging


class StationConnection:
    def __init__(
        self,
        hostname: str = "10.24.57.154:8000",
        api_key: str = "",
        ssl_verify: bool = False,
        logger: logging.Logger = None,
    ):
        self.rest_adapter: RestAdapter = RestAdapter(
            hostname, api_key, ssl_verify, logger
        )

    def execute_op(self, op: Operation, endpoint: str):
        data = {
            "id": str(op.id),
            "caller_id": str(op.caller_id),
            "method": op.method,
            "args": op.args,
        }
        
        return self.rest_adapter.post(endpoint=endpoint, data=data)
    

