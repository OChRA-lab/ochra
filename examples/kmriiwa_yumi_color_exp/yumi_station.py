# to add the parent directory to the path so we can import devices/robots folder
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from robots.abb_yumi.handler import YuMiRobot
from devices.web_camera.handler import WebCamera
from devices.tecan_xcalibur.handler import TecanXCalibur
from devices.ika_plate.handler import IkaPlate
from ochra.common.spaces.location import Location
from ochra.common.utils.enum import StationType
from ochra.manager.station.station_server import StationServer
from pathlib import Path


# construct station server
yumi_station = StationServer(
    name="yumi_station",
    location=Location(lab="ACL", room="main_lab", place="yumi_station"),
    station_type=StationType.WORK_STATION,
    station_port=8002,
    logging_path=Path(__file__).parent,
)

# setup the station server
yumi_station.setup(lab_ip="localhost:8001")

# construct devices
ika_plate = IkaPlate(name="ika_plate")
tecan_pump = TecanXCalibur(name="tecan_xcalibur_pump", reagents_map={"water": 1})
camera = WebCamera(name="camera", usb_port="ttyUSB0")

# construct robot
tasks = [
    "pick_vial_from_rack",
    "uncap_vial",
    "load_tecan_pump",
    "unload_tecan_pump",
    "load_ika_plate",
    "unload_ika_plate",
    "goto_camera_pose",
    "return_from_camera_pose",
    "cap_vial",
    "place_vial_in_rack",
]
yumi = YuMiRobot(name="yumi", available_tasks=tasks)

# add equipment to the station server
yumi_station.add_device(ika_plate)
yumi_station.add_device(tecan_pump)
yumi_station.add_device(camera)
yumi_station.add_device(yumi)

# run the station server
yumi_station.run()
