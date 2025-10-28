# to add the parent directory to the path so we can import devices/robots folder
import sys
import time
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ochra.discovery.storage.vessel import Vessel
from ochra.discovery.storage.reagent import Reagent
from ochra.discovery.spaces.lab import Lab
from ochra.discovery.storage.holder import Holder


# connect to lab
my_lab = Lab("127.0.0.1:8001")

# create a holder
rack = Holder(type="rack", max_capacity=6)
for i in range(6):
    vial = Vessel(type="vial", max_capacity=10, capacity_unit="ml")
    rack.add_container(vial)

# get station and add holder to its inventory
ika_station = my_lab.get_station("yumi_station")
ika_station.inventory.add_container(rack)

# remove vial from the rack
removed_vial = rack.containers[2]
rack.remove_container(vial)

# create reagents and add them to a vial
vial: Vessel = rack.containers[0]
reagent_1 = Reagent(name="water", amount=5, unit="ml")
reagent_2 = Reagent(name="red_dye", amount=5, unit="ml")
reagent_2.add_property("color", "red")
reagent_2.add_property("random", "0.5")
vial.add_reagent(reagent_1)
vial.add_reagent(reagent_2)

# remove reagent properties
reagent_2.remove_property("random")

