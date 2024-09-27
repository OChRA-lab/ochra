from ochra_manager.station.station import Station
from ochra_common.spaces.location import Location
from ika_plate.handler import IkaPlate as backendIkaPlate


mystation = Station(name="myStation", location=Location(
    name="myLocation", map="asd", map_id=123))
mystation.setup_server(lab_ip="localhost:8001")
myika = backendIkaPlate(name="amyIka", station_id=mystation.id)
mystation.add_device(myika)
mystation.run()
