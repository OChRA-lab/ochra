from ochra_common.connections.lab_connection import LabConnection
from ika_plate.device import IkaPlate

# connect to lab
mylabConnection = LabConnection("localhost:8001")

# get my ika plate
myIkaplate = IkaPlate(name="amyIka")

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
