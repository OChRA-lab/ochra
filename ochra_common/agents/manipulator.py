from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.agents.robot import Robot, RobotTask


@dataclass
class Manipulator(DataModel, Robot, ABC):
    tasks: list[RobotTask]
    
    @abstractmethod
    def execute(RobotTask) -> bool:
        pass
    