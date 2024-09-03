from pydantic import Field
from typing import Dict, Any
from uuid import UUID
from enum import Enum
from datetime import datetime
from ..base import DataModel


class Task(DataModel):
    """
    Abstract task class to hold all information about a task.

    Attributes:
        assignee_id (UUID): The unique identifier of the assignee.
        name (str): The name of the task.
        args (dict): A dictionary of arguments related to the task.
        status (Enum): The current status of the task.
        start_timestamp (datetime): The timestamp when the task started.
        end_timestamp (datetime): The timestamp when the task ended.
    """
    assignee_id: UUID
    name: str
    args: Dict[str, Any] = Field(default_factory=dict)
    status: Enum = -1  # TODO: Define Enum for task status
    start_timestamp: datetime = Field(default=None)
    end_timestamp: datetime = Field(default=None)
