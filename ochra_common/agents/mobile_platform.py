from abc import abstractmethod
from dataclasses import dataclass
from ochra_common.agents.robot import Robot, Location


@dataclass
class MobilePlatform(Robot):
    conditions: dict

    @abstractmethod
    def go_to(self, location: Location) -> bool:
        pass
