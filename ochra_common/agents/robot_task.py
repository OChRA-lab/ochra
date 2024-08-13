from dataclasses import dataclass
from ochra_common.agents.task import Task
from enum import Enum


@dataclass
class RobotTask(Task):
    priority: Enum
