"""Run the APC filtration work station."""

import os
import sys
from pathlib import Path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(r"C:\Users\ACL\ochra-apc-devices\ochra_apc_devices")


from ochra_apc_devices.devices.fume_hood_sash.handler import FumeHoodSash
from ochra_apc_devices.devices.filtration.handler import Filtration
from ochra.common.spaces.location import Location
from ochra.common.utils.enum import StationType
from ochra.manager.station.station_server import StationServer


# construct station server
APC_station = StationServer(
    name="APC_station",
    location=Location(lab="ACL", room="main_lab", place="APC_station"),
    station_type=StationType.WORK_STATION,
)

# setup the station server
APC_station.setup(lab_ip="138.253.127.183:8001")

# construct devices
sash_door = FumeHoodSash(name="sash_door")
filtration = Filtration(name="filtration")

APC_station.add_device(sash_door)
APC_station.add_device(filtration)

if __name__ == "__main__":
    # run the station server
    APC_station.run()    