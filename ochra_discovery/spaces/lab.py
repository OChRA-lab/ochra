from ochra_common.spaces.lab import Lab
from ochra_common.spaces.station import Station
from ochra_common.equipment.robot import Robot
from ochra_common.connections.lab_connection import LabConnection
from typing import List, Type, Union


class Lab(Lab):
    def __init__(self, hostname: str, experiment_id = None):
        """Connects to the lab and provides access to the stations and robots.

        Args:
            hostname (str): Ip address and port of the lab server.
            experiment_id (str, optional): ID of the experiment. Defaults to None.
        """
        self._lab_conn: LabConnection = LabConnection(hostname,experiment_id)

    def get_station(
        self, station_name: str
    ) -> Station:
        """Get a station object by name.

        Args:
            station_name (str): Name of the station to get.

        Returns:
            Station: The station object.
        """
        return self._lab_conn.get_object("lab/stations", station_name)

    def get_stations(self) -> List[Station]:
        """Get all the connected stations.

        Returns:
            List[Station]: list of station objects
        """
        return self._lab_conn.get_all_objects("lab/stations")

    def get_robot(self, robot_name: str) -> Type[Robot]:
        """get a robot object by name.

        Args:
            robot_name (str): Name of the robot to get.

        Returns:
            Type[Robot]: The robot object.
        """
        return self._lab_conn.get_object("lab/robots", robot_name)

    def get_robots(self) -> List[Type[Robot]]:
        """get a list of all the connected robots.

        Returns:
            List[Type[Robot]]: list of robot objects.
        """
        return self._lab_conn.get_all_objects("lab/robots")
