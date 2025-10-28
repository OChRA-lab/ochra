# to add the parent directory to the path so we can import devices/robots folder
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ochra.discovery.equipment.operation import Operation
from devices.web_camera.device import WebCamera
from ochra.discovery.spaces.lab import Lab
from ochra.discovery.equipment.operation_result import OperationResult
from time import sleep
from uuid import UUID
from ochra.discovery.utils.lock import lock

# connect to lab
my_lab = Lab("0.0.0.0:8001")

# get camera station
camera_station = my_lab.get_station("camera_station")

# get camera
try:
    my_camera: WebCamera = camera_station.get_device("my_horse")
except Exception as e:
    print(e)

my_camera: WebCamera = camera_station.get_device("my_camera")

try:
    error_op: Operation = my_camera.error()
except Exception as e:
    print(e)