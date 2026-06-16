"""Run the APC filtration work station."""

import os
import sys
from pathlib import Path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(r"C:\Users\ACL\ochra-apc-devices\ochra_apc_devices")


from ochra_apc_devices.devices.fume_hood_sash.handler import FumeHoodSash
from ochra.common.spaces.location import Location
from ochra.common.utils.enum import StationType
from ochra.manager.station.station_server import StationServer


# construct station server
sash_door_station = StationServer(
    name="sash_door_station",
    location=Location(lab="ACL", room="main_lab", place="sash_door_station"),
    station_type=StationType.WORK_STATION,
)

# setup the station server
sash_door_station.setup(lab_ip="138.253.127.183:8001")

# construct devices
sash_door = FumeHoodSash(name="sash_door")

sash_door_station.add_device(sash_door)

if __name__ == "__main__":
    # run the station server
    sash_door_station.run()    