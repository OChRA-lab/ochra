from ochra_common.connections.rest_adapter import RestAdapter, Result
from ochra_common.equipment.operation import Operation
import logging


class StationConnection:
    """
    Class that provides a high-level interface for interacting with a remote station, utilizing RestAdapter for communication.
    """

    def __init__(
        self,
        hostname: str = "10.24.57.154:8000",
        api_key: str = "",
        ssl_verify: bool = False,
    ):
        self._logger = logging.getLogger(__name__)
        self.rest_adapter: RestAdapter = RestAdapter(
            hostname, api_key, ssl_verify, self._logger
        )
        

    def execute_op(self, op: Operation, endpoint: str) -> Result:
        """
        Execute an operation on the remote station.

        Args:
            op (Operation): The operation to be executed.
            endpoint (str): The API endpoint for executing the operation.
        Returns:
            Result: The response from the remote station after executing the operation.
        """
        data = {
            "id": str(op.id),
            "collection": op.collection,
            "module_path": op.module_path,
            "entity_id": str(op.entity_id),
            "entity_type": op.entity_type,
            "caller_id": str(op.caller_id),
            "method": op.method,
            "args": op.args,
        }

        # Not possible to use op.model_dump(mode="json") because there are no optional
        # fields and thus None is not an allowed value for them
        return self.rest_adapter.post(endpoint=endpoint, data=data)
