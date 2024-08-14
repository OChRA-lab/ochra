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
    """Lab abstract class """
    stations: list[Station]
    agents: list[Agent]

    @abstractmethod
    def get_robots(self) -> list[Robot]:
        pass

    @abstractmethod
    def get_robot(self, robot: str | type | UUID) -> Robot:
        pass

    @abstractmethod
    def get_scientists(self) -> list[Scientist]:
        pass

    @abstractmethod
    def add_scientist(self, scientist: Scientist) -> bool:
        pass
