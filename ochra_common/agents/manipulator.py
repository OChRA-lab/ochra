from abc import abstractmethod
from dataclasses import dataclass
from ochra_common.agents.robot import Robot, RobotTask


@dataclass
class Manipulator(Robot):
    tasks: list[RobotTask]

    @abstractmethod
    def execute(self, robot_task: RobotTask) -> bool:
        pass
