from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from .task import Task
from enum import Enum


@dataclass
class Agent(DataModel):
    """Agent abstract class to represent a generic task executor
    """
    name: str
    status: Enum
    assigned_task: Task
    task_status: Enum
    tasks_history: list[Task]

    @abstractmethod
    def assign(self, task: Task) -> bool:
        pass
