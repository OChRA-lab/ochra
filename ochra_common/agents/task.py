from dataclasses import dataclass
from ..base import DataModel
from uuid import UUID
from enum import Enum
from datetime import datetime


@dataclass
class Task(DataModel):
    """
    Abstract task class to hold all information about a task.

    Attributes:
        asignee_id (UUID): The unique identifier of the assignee.
        name (str): The name of the task.
        _args (dict): A dictionary of arguments related to the task.
        status (Enum): The current status of the task.
        start_timestamp (datetime): The timestamp when the task started.
        end_timestamp (datetime): The timestamp when the task ended.
    """
    asignee_id: UUID
    name: str
    _args: dict
    status: Enum
    start_timestamp: datetime
    end_timestamp: datetime
