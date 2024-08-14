from abc import abstractmethod
from dataclasses import dataclass
from .robot import Robot
from .robot_task import RobotTask


@dataclass
class Manipulator(Robot):
    """
    Abstract manipulator robot that can execute tasks.

    Attributes:
        tasks (list[RobotTask]): A list of tasks assigned to the manipulator.
    """
    tasks: list[RobotTask]

    @abstractmethod
    def execute(self, robot_task: RobotTask) -> bool:
        """
        Execute a given robot task.

        Args:
            robot_task (RobotTask): The task to be executed.

        Returns:
            bool: True if the task was executed successfully
        """
        pass
