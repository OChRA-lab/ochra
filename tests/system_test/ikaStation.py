from ochra_manager.Station.communicator import Communicator
# create sample device
from ika_plate.handler import IkaPlate as backendIkaPlate


class myStation(Communicator):
    def setup(self):
        myika = backendIkaPlate(name="amyIka", station_id=self.station_id)
        self.devices.append(myika)


myStationInstance = myStation(lab_ip="localhost:8001")

myStationInstance.run()
