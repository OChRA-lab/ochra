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
from ochra_apc_devices.devices.base_valve.device import BaseValve
from ochra_apc_devices.devices.easy_sampler_vial_arm.device import EasySamplerVialArm
from ochra_apc_devices.devices.balance_door.device import BalanceDoor
from ochra_apc_devices.devices.tecan_xlp6000.device import TecanXLP6000
from ochra_apc_devices.devices.solid_addition.device import SolidAddition


# connect to lab
my_lab = Lab("138.253.127.183:8001")

# get station and needed equipment
sash_door_station: Station = my_lab.get_station("sash_door_station")
fume_hood_sash: FumeHoodSash = sash_door_station.get_device("sash_door")

filtration_station: Station = my_lab.get_station("filtration_station")
Filtration_device: Filtration = filtration_station.get_device("filtration")

base_valve_station: Station = my_lab.get_station("base_valve_station")
BaseValve_device: BaseValve = base_valve_station.get_device("base_valve")

Sample_vial_arm_station: Station = my_lab.get_station("Sample_vial_arm_station")
EasySamplerVialArm_device: EasySamplerVialArm = Sample_vial_arm_station.get_device("EasySamplerVialArm")

balance_door_station: Station = my_lab.get_station("balance_door_station")
BalanceDoor_device: BalanceDoor = balance_door_station.get_device("balance_door")

Syringe_pump_station: Station = my_lab.get_station("Syringe_pump_station")
TecanXLP6000_device: TecanXLP6000 = Syringe_pump_station.get_device("TecanXLP6000")

Solid_addition_station: Station = my_lab.get_station("solid_addition_station")
SolidAddition_device: SolidAddition = Solid_addition_station.get_device("solid_addition")

# kuka mobile station
kuka_mobile_station: Station = my_lab.get_station("kuka2_mobile_station")
kmriiwa: KukaKMRiiwa = kuka_mobile_station.get_robot("kuka2")

# Syringe pump dispense liquid.
print("Requesting pumping from TecanXLP6000...")
TecanXLP6000_device.request_pumping(withdraw_port=1, dispense_port=2, volume=25, speed=120)
time.sleep(3)

# Mock dispense of solid.
print("Requesting dispensing from SolidAddition...")
SolidAddition_device.extend_piston();time.sleep(1)
SolidAddition_device.dispense()
SolidAddition_device.retract_piston()
time.sleep(3)

# Move vial using pneumatic arm.
print("Requesting moving vial from EasySamplerVialArm...")
EasySamplerVialArm_device.home()
EasySamplerVialArm_device.move_vial()
time.sleep(3)

# Kuka mobile robot move to EasySampler station.
print("Kuka mobile robot moving to EasySampler station...")
kmriiwa.go_to({"graph_id": 1, "node_id": 48, "fine_localization": True})
time.sleep(3)

# Sash door lift up.
print("Sash door lift up...")
fume_hood_sash.move_up()
time.sleep(3)

# Kuka mobile robot pick up vial.
print("Kuka mobile robot picking up vial...")
kmriiwa.execute(task_name="TransferSampleVialToDeck", args={})
time.sleep(3)

# Sash door move down.
print("Sash door move down...")
fume_hood_sash.move_down()
time.sleep(3)

# Kuka mobile robot move to filtration station.
print("Kuka mobile robot moving to filtration station...")
kmriiwa.go_to({"graph_id": 1, "node_id": 49, "fine_localization": True})
time.sleep(3)

# Sash door lift up.
print("Sash door lift up...")
fume_hood_sash.move_up()
time.sleep(3)

# Kuka mobile robot place funnel.
print("Kuka mobile robot placing funnel...")
kmriiwa.execute(task_name="FunnelToFiltration", args={})
time.sleep(3)

# Sash door down.
print("Sash door down...")
fume_hood_sash.move_down()
time.sleep(3)

# Filtration - turn on vacuum to pull liquid through filter.
print("Turning on vacuum to pull liquid through filter...")
Filtration_device.open_vacuum_valve()
time.sleep(1)

# Open base valve to remove solvents.
print("Opening base valve to remove solvents...")
BaseValve_device.open_valve()
# time.sleep(3)

# Close base valve.
print("Closing base valve...")
BaseValve_device.close_valve()
time.sleep(10)


# Turn off vacuum.
print("Turning off vacuum...")
Filtration_device.close_vacuum_valve()
time.sleep(3)

# Sash door lift up.
print("Sash door lift up...")
fume_hood_sash.move_up()
time.sleep(3)

# Balance door open.
print("Balance door open...")
BalanceDoor_device.move_up()
time.sleep(3)

# Robot move to balance station.
print("Kuka mobile robot moving to balance station...")
kmriiwa.execute(task_name="FunnelToWeighing", args={})
time.sleep(3)

# Balance door close.
print("Balance door close...")
BalanceDoor_device.move_down()
time.sleep(3)

# Balance door open.
print("Balance door open...")
BalanceDoor_device.move_up()
time.sleep(3)

# Kuka mobile robot return funnel.
print("Kuka mobile robot returning funnel...")
kmriiwa.execute(task_name="FunnelBackToShelf", args={})
time.sleep(3)

# Balance door close.
print("Balance door close...")
BalanceDoor_device.move_down()
time.sleep(3)

# Kuka mobile robot back to the home location.
print("Kuka mobile robot moving back to the home location...")
kmriiwa.go_to({"graph_id": 1, "node_id": 31, "fine_localization": True})
time.sleep(3)

# Sash door down.
print("Sash door down...")
fume_hood_sash.move_down()
time.sleep(3)


