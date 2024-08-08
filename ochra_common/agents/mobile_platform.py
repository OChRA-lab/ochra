from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.agents.robot import Robot, Location


@dataclass
class MobilePlatform(DataModel, Robot, ABC):
    conditions: dict
    
    @abstractmethod
    def go_to(self, location: Location) -> bool:
        pass
    