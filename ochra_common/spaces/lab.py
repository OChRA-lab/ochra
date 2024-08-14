from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from .station import Station
from ..agents.agent import Agent
from ..agents.robot import Robot
from ..agents.scientist import Scientist
from uuid import UUID


@dataclass
class Lab(DataModel):
    """
    Abstract Lab class that represents a laboratory.

    Attributes:
        stations (list[Station]): A list of stations in the lab.
        agents (list[Agent]): A list of agents in the lab.
    """
    stations: list[Station]
    agents: list[Agent]

    @abstractmethod
    def get_robots(self) -> list[Robot]:
        """
        Retrieve all robots in the lab.

        Returns:
            list[Robot]: A list of robots in the lab.
        """
        pass

    @abstractmethod
    def get_robot(self, robot: str | type | UUID) -> Robot:
        """
        Retrieve a specific robot from the lab.

        Args:
            robot (str | type | UUID): The name, type, or UUID of the robot.

        Returns:
            Robot: The retrieved robot.
        """
        pass

    @abstractmethod
    def get_scientists(self) -> list[Scientist]:
        """
        Retrieve all scientists in the lab.

        Returns:
            list[Scientist]: A list of scientists in the lab.
        """
        pass

    @abstractmethod
    def add_scientist(self, scientist: Scientist) -> bool:
        """
        Add a scientist to the lab.

        Args:
            scientist (Scientist): The scientist to be added.

        Returns:
            bool: True if the scientist was added successfully, False otherwise.
        """
        pass
