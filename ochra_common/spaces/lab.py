from abc import abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.spaces.station import Station
from ochra_common.agents.agent import Agent
from ochra_common.agents.robot import Robot
from ochra_common.agents.scientist import Scientist


@dataclass
class Lab(DataModel):
    stations: list[Station]
    agents: list[Agent]

    @abstractmethod
    def get_robots(self) -> list[Robot]:
        pass

    @abstractmethod
    def getrobot(self, robot: str | type) -> Robot:
        pass

    @abstractmethod
    def get_scientists(self) -> list[Scientist]:
        pass

    @abstractmethod
    def add_scientist(self, scientist: Scientist) -> bool:
        pass
