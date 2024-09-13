from ochra_manager.Station.communicator import Communicator
# create sample device
from ika_plate.handler import IkaPlate as backendIkaPlate
from ochra_common.spaces.work_station import WorkStation
from ochra_common.spaces.location import Location

class myStation(Communicator,WorkStation):
    # setup the station
    def setup(self):
        # create a device
        myika = backendIkaPlate(name="amyIka", station_id=self._station_id)
        # add the device to the stations devices list
        self.devices.append(myika)

#create station
myLocation = Location(name="amyLocation",map="asd",map_id=123)
myStationInstance = myStation(name="amyStation",location=myLocation)
myStationInstance.setup_server(lab_ip="localhost:8001")
myStationInstance.run()
