from abc import abstractmethod
from dataclasses import dataclass
from .robot import Robot
from ..spaces.location import Location


@dataclass
class MobilePlatform(Robot):
    conditions: dict

    @abstractmethod
    def go_to(self, location: Location) -> bool:
        pass
