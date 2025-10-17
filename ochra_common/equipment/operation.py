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
    """

    caller_id: str
    """Unique identifier of the caller initiating the operation."""

    entity_id: uuid.UUID
    """Unique identifier of the target entity."""

    entity_type: str
    """Type of the entity (e.g., 'device', 'station')."""

    method: str
    """Name of the method invoked."""

    args: Dict[str, Any]
    """Arguments passed to the method."""

    status: OperationStatus = OperationStatus.CREATED
    """Current status of the operation. Defaults to CREATED."""

    start_timestamp: datetime = Field(default=None)
    """ Timestamp when the operation started."""

    end_timestamp: datetime = Field(default=None)
    """ Timestamp when the operation ended."""

    result: OperationResult = Field(default=None)
    """Result of the operation."""

    _endpoint = "operations"  # associated endpoint for all operations
