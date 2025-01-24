from typing import List, Dict, Any
from .device import Device


class Robot(Device):
    """
    Abstract robot class to represent a generic robot.

    Attributes:
        available_tasks (List[str]): A list of tasks available for execution by the robot.
    """

    available_tasks: List[str]

    _endpoint = "robots"  # associated endpoint for all robots

    def execute(self, task_name: str, args: Dict[str, Any]) -> bool:
        """
        Execute a given robot task.

        Args:
            robot_task (RobotTask): The task to be executed.

        Returns:
            bool: True if the task was executed successfully
        """
        raise NotImplementedError
