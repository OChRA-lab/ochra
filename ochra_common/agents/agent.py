from enum import Enum
from pydantic import Field
from typing import List
from ..base import DataModel
from .task import Task


class Agent(DataModel):
    """
    Agent abstract class to represent a generic task executor.

    Attributes:
        name (str): The name of the agent.
        status (Enum): The current status of the agent.
        assigned_task (Task): The task currently assigned to the agent.
        tasks_history (List[Task]): A history of tasks assigned to the agent.
    """
    name: str
    status: Enum = -1  # TODO: Define Enum for agent status
    assigned_task: Task = Field(default=None)
    tasks_history: List[Task] = Field(default_factory=list)

    def assign(self, task: Task) -> bool:
        """
        Assign a task to the agent.

        Args:
            task (Task): The task to be assigned.

        Returns:
            bool: True if the task was assigned successfully, False otherwise.
        """
        raise NotImplementedError
