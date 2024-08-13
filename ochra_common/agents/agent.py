from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.agents.task import Task
from enum import Enum


@dataclass
class Agent(DataModel):
    name: str
    status: Enum
    assigned_task: Task
    task_status: Enum
    tasks_history: list[Task]

    @abstractmethod
    def assign(self, task: Task) -> bool:
        pass
