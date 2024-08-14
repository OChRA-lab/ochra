from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from .task import Task
from enum import Enum


@dataclass
class Agent(DataModel):
    """
    Agent abstract class to represent a generic task executor.

    Attributes:
        name (str): The name of the agent.
        status (Enum): The current status of the agent.
        assigned_task (Task): The task currently assigned to the agent.
        task_status (Enum): The status of the assigned task.
        tasks_history (list[Task]): A history of tasks assigned to the agent.
    """
    name: str
    status: Enum
    assigned_task: Task
    task_status: Enum
    tasks_history: list[Task]

    @abstractmethod
    def assign(self, task: Task) -> bool:
        """
        Assign a task to the agent.

        Args:
            task (Task): The task to be assigned.

        Returns:
            bool: True if the task was assigned successfully, False otherwise.
        """
        pass
