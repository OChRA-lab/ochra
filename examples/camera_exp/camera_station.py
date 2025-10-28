# We will create a station server with a single IkaPlate device.

# to add the parent directory to the path so we can import devices/robots folder
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ochra.manager.station.station_server import StationServer
from ochra.common.spaces.location import Location
from ochra.common.utils.enum import StationType
from devices.web_camera.handler import WebCamera
from pathlib import Path

# construct station server
my_station = StationServer(
    name="camera_station",
    station_type=StationType.WORK_STATION,
    location=Location(lab="ACL", room="main_lab", place="yumi_station"),
    logging_path=Path(__file__).parent,
)

# setup the station server
my_station.setup(lab_ip="localhost:8001")

# construct device
camera = WebCamera(name="my_camera")

# add device to the station server
my_station.add_device(camera)

# run the station server
my_station.run()
