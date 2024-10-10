from ochra_manager.Station.station_server import StationServer
from ochra_common.spaces.location import Location
from ika_plate.handler import IkaPlate as backendIkaPlate

# construct station server
my_station = StationServer(name="myStation", location=Location(
    name="myLocation", map="asd", map_id=123))

# setup the station server
my_station.setup(lab_ip="localhost:8001")

# construct device
ika = backendIkaPlate(name="yumi_ika", station_id=my_station._station_proxy.id)

# add device to the station server
my_station.add_device(ika)

# run the station server
my_station.run()
