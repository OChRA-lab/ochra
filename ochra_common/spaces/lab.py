from typing import List, Type, Union
from .station import Station
from ..agents.robot import Robot
from ..agents.scientist import Scientist
from uuid import UUID


class Lab:
    """
    Abstract Lab class that represents a laboratory.
    """

    def get_stations(self) -> List[Type[Station]]:
        """
        Retrieve all stations in the lab.

        Returns:
            List[Station]: A list of stations in the lab.
        """
        raise NotImplementedError

    def get_station(self, station_name: str) -> Type[Station]:
        """
        Retrieve a specific station from the lab.

        Args:
            station_name (str): The name of the station.

        Returns:
            Station: The retrieved station.
        """
        raise NotImplementedError

    def get_robots(self) -> List[Type[Robot]]:
        """
        Retrieve all robots in the lab.

        Returns:
            List[Robot]: A list of robots in the lab.
        """
        raise NotImplementedError

    def get_robot(self, robot: Union[str, Type[Robot], UUID]) -> Type[Robot]:
        """
        Retrieve a specific robot from the lab.

        Args:
            robot (str | type | UUID): The name, type, or UUID of the robot.

        Returns:
            Robot: The retrieved robot.
        """
        raise NotImplementedError

    def get_scientists(self) -> List[Scientist]:
        """
        Retrieve all scientists in the lab.

        Returns:
            List[Scientist]: A list of scientists in the lab.
        """
        raise NotImplementedError

    def add_scientist(self, scientist: Scientist) -> bool:
        """
        Add a scientist to the lab.

        Args:
            scientist (Scientist): The scientist to be added.

        Returns:
            bool: True if the scientist was added successfully, False otherwise.
        """
        raise NotImplementedError

    def remove_scientist(self, scientist: Scientist) -> bool:
        """
        Remove a scientist from the lab.

        Args:
            scientist (Scientist): The scientist to be removed.

        Returns:
            bool: True if the scientist was removed successfully, False otherwise.
        """
        raise NotImplementedError
