from typing import List, Dict, Any
from .device import Device


class Robot(Device):
    """
    Abstract class to represent a generic robot.
    """

    available_tasks: List[str]
    """A list of tasks available for execution by the robot."""

    _endpoint = "robots"  # associated endpoint for all robots

    def execute(self, task_name: str, args: Dict[str, Any]) -> bool:
        """
        Executes a specified task on the robot.

        Args:
            task_name (str): The name of the task to execute.
            args (Dict[str, Any]): Arguments required for the task execution.

        Returns:
            bool: True if the task was executed successfully, False otherwise.
        """
        raise NotImplementedError
