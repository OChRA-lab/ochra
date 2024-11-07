from .task import Task
from enum import Enum


class RobotTask(Task):
    """
    Abstract task specifically for robots.

    Attributes:
        priority (Enum): The priority level of the task.
    """

    priority: Enum = -1  # TODO: Define Enum for robot task priority
