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
from ochra.discovery.storage.holder import Holder

from devices.ika_plate.device import IkaPlate
from devices.tecan_xcalibur.device import TecanXCalibur
from devices.web_camera.device import WebCamera
from robots.abb_yumi.device import YuMiRobot


# connect to lab
my_lab = Lab("127.0.0.1:8001")

# create a holder
rack = Holder(type="rack", max_capacity=6)
for i in range(6):
    vial = Vessel(type="vial", max_capacity=10, capacity_unit="ml")
    rack.add_container(vial)

# get station and needed equipment
ika_station = my_lab.get_station("yumi_station")
tecan_pump: TecanXCalibur = ika_station.get_device("tecan_xcalibur_pump")
ika_plate: IkaPlate = ika_station.get_device("ika_plate")
camera: WebCamera = ika_station.get_device("camera")
yumi: YuMiRobot = ika_station.get_robot("yumi")

# add holder to station
ika_station.inventory.add_container(rack)
images = []
vial: Vessel
for i, vial in enumerate(rack.containers):
    # pick up vial and decap
    yumi.execute("pick_vial_from_input_loc", {"vial_index": i})
    yumi.execute("decap", {})

    # move vial to pump and dispense water
    yumi.execute("place_vial_in_pump", {})
    tecan_pump.dispense("water", 10, "ml")
    added_reagent = Reagent("water", 10, "ml")
    vial.add_reagent(added_reagent)

    # move vial from pump to ika
    yumi.execute("pick_vial_from_pump", {})
    yumi.execute("place_vial_in_ika", {})

    # stir for 1 seconds
    ika_plate.set_speed(100)
    ika_plate.start_stir()
    time.sleep(1)
    ika_plate.stop_stir()

    # move vial from ika to camera
    yumi.execute("pick_vial_from_ika", {})
    yumi.execute("place_vial_in_camera", {})

    # take image and store to list
    op: Operation = camera.take_image()
    img = op.result if op.result else "no image"
    images.append(img)

    yumi.execute("pick_vial_from_camera", {})
    yumi.execute("cap", {})
    yumi.execute("place_vial_in_output_loc", {"vial_index": i})

# do something with images
print(images)
