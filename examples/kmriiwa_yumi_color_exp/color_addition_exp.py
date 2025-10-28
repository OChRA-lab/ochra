# to add the parent directory to the path so we can import devices/robots folder
import sys
import time
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ochra.discovery.storage.vessel import Vessel
from ochra.discovery.storage.reagent import Reagent
from ochra.discovery.equipment.operation import Operation
from ochra.discovery.spaces.lab import Lab
from ochra.discovery.spaces.station import Station
from ochra.common.spaces.location import Location
from ochra.discovery.storage.holder import Holder
from ochra.discovery.equipment.operation_result import OperationResult
from uuid import UUID

from devices.ika_plate.device import IkaPlate
from devices.tecan_xcalibur.device import TecanXCalibur
from devices.web_camera.device import WebCamera
from robots.abb_yumi.device import YuMiRobot
from robots.kuka_kmriiwa.device import KukaKMRiiwa

# connect to lab
my_lab = Lab("localhost:8001")

# create a holder
rack = Holder(type="rack", max_capacity=8)
for i in range(2):
    vial = Vessel(type="vial", max_capacity=20, capacity_unit="ml")
    rack.add_container(vial)

# get station and needed equipment
# kuka mobile station
kuka_mobile_station: Station = my_lab.get_station("kuka_mobile_station")
kmriiwa: KukaKMRiiwa = kuka_mobile_station.get_robot("kmriiwa")

# yumi station
yumi_station: Station = my_lab.get_station("yumi_station")
xcalibur_pump: TecanXCalibur = yumi_station.get_device("tecan_xcalibur_pump")
ika_plate: IkaPlate = yumi_station.get_device("ika_plate")
camera: WebCamera = yumi_station.get_device("camera")
yumi: YuMiRobot = yumi_station.get_robot("yumi")


# load rack to the yumi station
# add holder to station
kuka_mobile_station.inventory.add_container(rack)

# move rack to yumi station
# yumi_station_loc = yumi_station.location

kmriiwa.go_to({"graph_id": 1, "node_id": 30, "fine_localization": True})
kmriiwa.execute("PickPlaceRackDeckToStation", {})
kmriiwa.go_to({"graph_id": 1, "node_id": 24, "fine_localization": False})

# add holder to station
kuka_mobile_station.inventory.remove_container(rack)
yumi_station.inventory.add_container(rack)

# fill the vials with liquid and image them
images = []
vial: Vessel
for i, vial in enumerate(rack.containers):
    # pick up vial and decap
    yumi.execute("pick_vial_from_rack", {"index": i})
    yumi.execute("uncap_vial", {})

    # move vial to pump and dispense water
    yumi.execute("load_tecan_pump", {})
    xcalibur_pump.dispense("water", 10, "ml")
    added_reagent = Reagent("water", 10, "ml")
    vial.add_reagent(added_reagent)

    # take vial from pump and cap
    yumi.execute("unload_tecan_pump", {})
    yumi.execute("cap_vial", {})

    # move vial to ika to stir
    yumi.execute("load_ika_plate", {})

    # stir for 1 seconds
    ika_plate.set_speed(100)
    ika_plate.start_stir()
    time.sleep(1)
    ika_plate.stop_stir()

    # unload vial from ika plate and move top.result if op.result else "no image"o camera
    yumi.execute("unload_ika_plate", {})
    yumi.execute("goto_camera_pose", {})

    # take image and store to list
    op: Operation = camera.take_image()
    img = op.result if op.result else "no image"
    images.append(img)

    # move vial back to rack
    yumi.execute("return_from_camera_pose", {})
    yumi.execute("place_vial_in_rack", {"index": i})

# do something with images
print("================== images ==================")
print(images)
print("====================================")

# move rack back to kuka station
kmriiwa.go_to({"graph_id": 1, "node_id": 30, "fine_localization": True})
kmriiwa.execute("PickPlaceRackStationToDeck", {})
kmriiwa.go_to({"graph_id": 1, "node_id": 24, "fine_localization": False})
yumi_station.inventory.remove_container(rack)
kuka_mobile_station.inventory.add_container(rack)
