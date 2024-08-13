from dataclasses import dataclass
from .task import Task
from enum import Enum


@dataclass
class RobotTask(Task):
    priority: Enum
