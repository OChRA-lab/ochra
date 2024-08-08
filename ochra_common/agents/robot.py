from abc import ABC
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.agents.task import Task
from enum import Enum


@dataclass
class RobotTask(DataModel, ABC, Task):
    priority: Enum