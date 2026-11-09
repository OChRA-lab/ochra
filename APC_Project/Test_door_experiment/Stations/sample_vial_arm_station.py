"""Run the APC filtration work station."""

import os
import sys
from pathlib import Path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(r"C:\Users\ACL\ochra-apc-devices\ochra_apc_devices")


# from ochra_apc_devices.devices.fume_hood_sash.handler import FumeHoodSash
from ochra_apc_devices.devices.easy_sampler_vial_arm.handler import EasySamplerVialArm
from ochra.common.spaces.location import Location
from ochra.common.utils.enum import StationType
from ochra.manager.station.station_server import StationServer


# construct station server
Sample_vial_arm_station = StationServer(
    name="Sample_vial_arm_station",
    location=Location(lab="ACL", room="main_lab", place="Sample_vial_arm_station"),
    station_type=StationType.WORK_STATION,station_port=8007
)

# setup the station server
Sample_vial_arm_station.setup(lab_ip="138.253.127.183:8001")

# construct devices
arm = EasySamplerVialArm(name="EasySamplerVialArm")

Sample_vial_arm_station.add_device(arm)

if __name__ == "__main__":
    # run the station server
    Sample_vial_arm_station.run()    