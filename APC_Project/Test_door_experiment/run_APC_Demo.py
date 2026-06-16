import os
import sys
import time

# ensure project root is on sys.path so top-level packages (like `devices`) import
# correctly when running this script from its directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(r"C:\Users\ACL\ochra-apc-devices\ochra_apc_devices")

from ochra.discovery.storage.vessel import Vessel
from ochra.discovery.storage.reagent import Reagent
from ochra.discovery.equipment.operation import Operation
from ochra.discovery.spaces.lab import Lab
from ochra.discovery.spaces.station import Station
from ochra.common.spaces.location import Location
from ochra.discovery.storage.holder import Holder
from ochra.discovery.equipment.operation_result import OperationResult
from uuid import UUID

from kuka_kmriiwa.device import KukaKMRiiwa
from devices.fume_hood_sash.device import FumeHoodSash
from ochra_apc_devices.devices.filtration.device import Filtration


# connect to lab
my_lab = Lab("138.253.127.183:8001")

# get station and needed equipment
# APC_station: Station = my_lab.get_station("APC_station")
sash_door_station: Station = my_lab.get_station("sash_door_station")
fume_hood_sash: FumeHoodSash = sash_door_station.get_device("sash_door")

filtration_station: Station = my_lab.get_station("filtration_station")
Filtration_device: Filtration = filtration_station.get_device("filtration")

# kuka mobile station
kuka_mobile_station: Station = my_lab.get_station("kuka2_mobile_station")
kmriiwa: KukaKMRiiwa = kuka_mobile_station.get_robot("kuka2")

#Sash door lift up
fume_hood_sash.move_up()

#Kuka mobile robot move to filtration station
kmriiwa.go_to({"graph_id": 1, "node_id": 24, "fine_localization": False})

#kuka mobile robot place funnel

#open base valve to remove solvents

#close base valve

# filtration - turn on vacuum to pull liquid through filter
Filtration_device.open_vacuum_valve()

#turn off vacuum
Filtration_device.close_vacuum_valve()

#Kuka mobile robot return funnel

##Kuka mobile robot back to the home location
kmriiwa.go_to({"graph_id": 1, "node_id": 16, "fine_localization": False})

#sash door down
fume_hood_sash.move_down()

