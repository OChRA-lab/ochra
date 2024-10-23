from ochra_common.connections.lab_connection import LabConnection
from ika_plate.device import IkaPlate

# connect to lab
mylabConnection: LabConnection = LabConnection("localhost:8001")

# get my ika plate
myIkaplate = mylabConnection.get_object("devices", "yumi_ika")

# try to set (frontend)
myIkaplate.status = "idle"

# get status
print(myIkaplate.status)

# get temperature to verify it changes
print(myIkaplate.temperature)

# try to set temperature with method
print(myIkaplate.set_temperature(temperature=100))

# get temperature to verify it has changed
print(myIkaplate.temperature)

################################################

lab = Lab(address="localhost:8001")
yumi_station = lab.get_station("yumi_station")
yumi = yumi_station.get_robot("yumi")
ika_plate: IkaPlate = yumi_station.get_device("ika_plate")
vial = Vessel("vial")

yumi.execute("home")
yumi.execute("move_vial")
ika_plate.add_vial(vial)
op_result: OperationResult = ika_plate.set_temperature(100)
