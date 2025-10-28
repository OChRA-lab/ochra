# to add the parent directory to the path so we can import devices/robots folder
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from robots.kuka_kmriiwa.handler import KukaKMRiiwa
from ochra.common.spaces.location import Location
from ochra.common.utils.enum import StationType
from ochra.manager.station.station_server import StationServer
from pathlib import Path


# construct station server
kuka_station = StationServer(
    name="kuka_mobile_station",
    location=Location(lab="ACL", room="main_lab", place="bench_23"),
    station_type=StationType.MOBILE_ROBOT_STATION,
    station_port=8003,
    logging_path=Path(__file__).parent,
)

# setup the station server
kuka_station.setup(lab_ip="localhost:8001")

# construct robot
tasks = [
    "PickPlaceRackDeckToStation",
    "PickPlaceRackStationToDeck",
]
kmriiwa = KukaKMRiiwa(name="kmriiwa", available_tasks=tasks)

# add equipment to the station server
kuka_station.add_device(kmriiwa)

# run the station server
kuka_station.run()
