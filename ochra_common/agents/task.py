from dataclasses import dataclass
from ochra_common.base import DataModel
from uuid import UUID
from enum import Enum
from datetime import datetime


@dataclass
class Task(DataModel):
    asignee_id: UUID
    name: str
    _args: dict
    status: Enum
    start_timestamp: datetime
    end_timestamp: datetime
