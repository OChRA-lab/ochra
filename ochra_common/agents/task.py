from abc import ABC
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.agents.agent import Agent
from enum import Enum
from datetime import datetime



@dataclass
class Task(DataModel, ABC):
    asignee: Agent
    name: str
    _args: dict
    status: Enum
    start_timestamp: datetime
    end_timestamp: datetime