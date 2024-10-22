from ochra_common.spaces.lab import Lab
from ochra_common.spaces.work_station import WorkStation
from ochra_common.spaces.storage_station import StorageStation
from ochra_common.agents.robot import Robot
from ochra_common.connections.lab_connection import LabConnection
from typing import List, Type, Union


class Lab(Lab):
    def __init__(self, hostname: str):
        self._lab_conn: LabConnection = LabConnection(hostname)

    def get_station(self, station_name: str) -> Union[WorkStation, StorageStation]:
        return self._lab_conn.get_object("lab/stations", station_name)

    def get_stations(self) -> List[Union[WorkStation, StorageStation]]:
        return self._lab_conn.get_all_objects("lab/stations")

    def get_robot(self, robot_name: str) -> Type[Robot]:
        return self._lab_conn.get_object("lab/robots", robot_name)

    def get_stations(self) -> List[Type[Robot]]:
        return self._lab_conn.get_all_objects("lab/robots")
