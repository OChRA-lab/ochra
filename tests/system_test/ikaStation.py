from ochra_manager.Station.communicator import Communicator
# create sample device
from ika_plate.handler import IkaPlate as backendIkaPlate


class myStation(Communicator):
    # setup the station
    def setup(self):
        # create a device
        myika = backendIkaPlate(name="amyIka", station_id=self.station_id)
        # add the device to the stations devices list
        self.devices.append(myika)

#create station
myStationInstance = myStation(lab_ip="localhost:8001")

myStationInstance.run()
