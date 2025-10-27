from typing import List, Type, Union
from .station import Station
from ..equipment.robot import Robot
from uuid import UUID


class Lab:
    """
    Represents a laboratory containing stations and robots.

    This class provides methods to retrieve and manage stations and robots
    within the laboratory environment.
    """

    def get_stations(self) -> List[Station]:
        """
        Retrieve all stations in the lab.

        Returns:
            List[Station]: A list of stations in the lab.
        """
        raise NotImplementedError

    def get_station(self, station_name: str) -> Station:
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
            List[Type[Robot]]: A list of robots in the lab.
        """
        raise NotImplementedError

    def get_robot(self, robot: str | Type[Robot] | UUID) -> Type[Robot]:
        """
        Retrieve a specific robot from the lab.

        Args:
            robot (str | type | UUID): The name, type, or UUID of the robot.

        Returns:
            Type[Robot]: The retrieved robot.
        """
        raise NotImplementedError
