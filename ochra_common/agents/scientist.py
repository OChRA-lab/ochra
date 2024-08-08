from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.agents.agent import Agent
from enum import Enum


@dataclass
class Scientist(DataModel, Agent, ABC):
    _privilege: Enum
    
    @abstractmethod
    def complete_assigned_task() -> bool:
        pass
        