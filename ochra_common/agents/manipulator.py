from abc import abstractmethod
from dataclasses import dataclass
from .robot import Robot
from .robot_task import RobotTask


@dataclass
class Manipulator(Robot):
    tasks: list[RobotTask]

    @abstractmethod
    def execute(self, robot_task: RobotTask) -> bool:
        pass
