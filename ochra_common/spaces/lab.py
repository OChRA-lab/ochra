from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List
from ..base import DataModel
from .station import Station
from ..agents.agent import Agent
from ..agents.robot import Robot
from ..agents.scientist import Scientist
from uuid import UUID

_COLLECTION = "labs"


@dataclass(kw_only=True)
class Lab(DataModel):
    """
    Abstract Lab class that represents a laboratory.

    Attributes:
        stations (List[Station]): A list of stations in the lab.
        agents (List[Agent]): A list of agents in the lab.
    """
    stations: List[Station] = field(default_factory=list)
    agents: List[Agent] = field(default_factory=list)

    def __post_init__(self):
        self._collection = _COLLECTION
        return super().__post_init__()

    @abstractmethod
    def get_robots(self) -> List[Robot]:
        """
        Retrieve all robots in the lab.

        Returns:
            List[Robot]: A list of robots in the lab.
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
    def get_scientists(self) -> List[Scientist]:
        """
        Retrieve all scientists in the lab.

        Returns:
            List[Scientist]: A list of scientists in the lab.
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
