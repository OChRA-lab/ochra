from dataclasses import dataclass
from .task import Task
from enum import Enum


@dataclass
class RobotTask(Task):
    """
    Abstract task specifically for robots.

    Attributes:
        priority (Enum): The priority level of the task.
    """
    priority: Enum
