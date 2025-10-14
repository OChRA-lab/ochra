from pydantic import Field
import uuid
from datetime import datetime
from typing import Dict, Any
from ..base import DataModel
from ..utils.enum import OperationStatus
from .operation_result import OperationResult


class Operation(DataModel):
    """
    Represents an operation executed by a device.

    Attributes:
        caller_id (str): Unique identifier of the caller initiating the operation.
        entity_id (uuid.UUID): Unique identifier of the target entity.
        entity_type (str): Type of the entity (e.g., 'device', 'station').
        method (str): Name of the method invoked.
        args (Dict[str, Any]): Arguments passed to the method.
        status (OperationStatus): Current status of the operation. Defaults to CREATED.
        start_timestamp (datetime): Timestamp when the operation started.
        end_timestamp (datetime): Timestamp when the operation ended.
        result (OperationResult): Result of the operation.
    """

    caller_id: str
    entity_id: uuid.UUID
    entity_type: str
    method: str
    args: Dict[str, Any]
    status: OperationStatus = OperationStatus.CREATED
    start_timestamp: datetime = Field(default=None)
    end_timestamp: datetime = Field(default=None)
    result: OperationResult = Field(default=None)

    _endpoint = "operations"  # associated endpoint for all operations
