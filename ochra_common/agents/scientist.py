from .agent import Agent
from enum import Enum


class Scientist(Agent):
    """
    Abstract human scientist agent so we can have humans do tasks.

    Attributes:
        privilege (Enum): The privilege level of the scientist.
    """

    privilege: Enum = -1  # TODO: Define Enum for scientist privilege

    def complete_assigned_task(self) -> bool:
        """
        Complete the assigned task.

        Returns:
            bool: True if the task was completed successfully, False otherwise.
        """
        raise NotImplementedError
