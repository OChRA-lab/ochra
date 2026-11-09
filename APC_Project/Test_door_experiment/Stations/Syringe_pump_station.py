"""Run the APC filtration work station."""

import os
import sys
from pathlib import Path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(r"C:\Users\ACL\ochra-apc-devices\ochra_apc_devices")


from ochra_apc_devices.devices.tecan_xlp6000.handler import TecanXLP6000
from ochra.common.spaces.location import Location
from ochra.common.utils.enum import StationType
from ochra.manager.station.station_server import StationServer


# construct station server
Syringe_pump_station = StationServer(
    name="Syringe_pump_station",
    location=Location(lab="ACL", room="main_lab", place="Syringe_pump_station"),
    station_type=StationType.WORK_STATION, station_port=8002
)

# setup the station server
Syringe_pump_station.setup(lab_ip="138.253.127.183:8001")

# construct devices
syringe_pump = TecanXLP6000(name="TecanXLP6000", port="COM5", switch_address="0")

Syringe_pump_station.add_device(syringe_pump)

if __name__ == "__main__":
    # run the station server
    Syringe_pump_station.run()    