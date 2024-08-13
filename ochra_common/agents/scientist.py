from abc import abstractmethod
from dataclasses import dataclass
from .agent import Agent
from enum import Enum


@dataclass
class Scientist(Agent):
    _privilege: Enum

    @abstractmethod
    def complete_assigned_task(self) -> bool:
        pass
