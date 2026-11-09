"""Run the APC shared COM4 station for base valve and solid addition."""

import os
import sys
from pathlib import Path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(r"C:\Users\ACL\ochra-apc-devices\ochra_apc_devices")


from ochra_apc_devices.devices.base_valve.handler import BaseValve
from ochra_apc_devices.devices.solid_addition.handler import SolidAddition
from ochra.common.spaces.location import Location
from ochra.common.utils.enum import StationType
from ochra.manager.station.station_server import StationServer


# construct station server
base_valve_station = StationServer(
    name="base_valve_station",
    location=Location(lab="ACL", room="main_lab", place="base_valve_station"),
    station_type=StationType.WORK_STATION, station_port=8006
)

# setup the station server
base_valve_station.setup(lab_ip="138.253.127.183:8001")

# construct devices
base_valve = BaseValve(name="base_valve", port="COM4")
solid_addition = SolidAddition(
    name="solid_addition",
    address="192.168.1.52",
    port=5000,
    serial_port="COM4",
)

base_valve_station.add_device(base_valve)
base_valve_station.add_device(solid_addition)

if __name__ == "__main__":
    # run the station server
    base_valve_station.run()    
