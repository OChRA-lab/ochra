from typing import List, Dict, Any
from .robot import Robot
from .robot_task import RobotTask


class Manipulator(Robot):
    """
    Abstract manipulator robot that can execute tasks.

    Attributes:
        tasks (List[RobotTask]): A list of tasks assigned to the manipulator.
    """

    available_tasks: List[str]

    def execute(self, task_name: str, args: Dict[str, Any]) -> bool:
        """
        Execute a given robot task.

        Args:
            robot_task (RobotTask): The task to be executed.

        Returns:
            bool: True if the task was executed successfully
        """
        raise NotImplementedError
