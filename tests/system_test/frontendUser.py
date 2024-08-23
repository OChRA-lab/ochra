from ochra_common.connections.lab_connection import LabConnection
from ika_plate.device import IkaPlate as frontendIkaPlate

mylabConnection = LabConnection("localhost:8001")
myIkaplate = frontendIkaPlate(name="amyIka")
myIkaplate.status = "idle"
print(myIkaplate.status)
print(myIkaplate.temperature)
print(myIkaplate.set_temperature(temperature=100))
print(myIkaplate.temperature)
