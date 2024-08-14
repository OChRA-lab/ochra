from abc import abstractmethod
from dataclasses import dataclass
from .agent import Agent
from enum import Enum


@dataclass
class Scientist(Agent):
    """Abstract human scientist agent so we can have humans do tasks"""
    _privilege: Enum

    @abstractmethod
    def complete_assigned_task(self) -> bool:
        pass
