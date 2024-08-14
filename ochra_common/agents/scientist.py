from abc import abstractmethod
from dataclasses import dataclass
from .agent import Agent
from enum import Enum


@dataclass
class Scientist(Agent):
    """
    Abstract human scientist agent so we can have humans do tasks.

    Attributes:
        _privilege (Enum): The privilege level of the scientist.
    """
    _privilege: Enum

    @abstractmethod
    def complete_assigned_task(self) -> bool:
        """
        Complete the assigned task.

        Returns:
            bool: True if the task was completed successfully, False otherwise.
        """
        pass
