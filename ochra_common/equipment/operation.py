from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
import uuid
from enum import Enum
from datetime import datetime
from ochra_common.equipment.operation_result import OperationResult

@dataclass
class Operation(DataModel):
    _caller: uuid
    _method: str
    _args: dict
    status: Enum
    start_timestamp: datetime
    end_timestamp: datetime
    result: list[OperationResult]