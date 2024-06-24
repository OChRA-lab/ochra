from ochra_chem_engine.singleton import SingletonMeta
from ochra_chem_engine.rest_adapter import RestAdapter, Result, LabEngineException
import logging


class StationConnection():
    def __init__(
        self,
        hostname: str = "10.24.57.154:8000",
        api_key: str = "",
        ssl_verify: bool = False,
        logger: logging.Logger = None,
    ):
        self.rest_adapter = RestAdapter(hostname, api_key, ssl_verify, logger)

    def execute_op(self, op, deviceName, **kwargs):
        data = {"operation": op,
                "deviceName": deviceName,
                "args": kwargs}
        return self.rest_adapter.post(endpoint="process_op", data=data)
