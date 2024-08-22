from ochra_common.spaces.location import Location
from ochra_common.spaces.station import Station
from ochra_common.spaces.work_station import WorkStation
from ochra_common.spaces.storage_station import StorageStation
from ochra_common.spaces.lab import Lab


def test_location():
    # test construction of the location
    location = Location(
        name="test_location",
        map="test_map",
        map_id=1,
    )

    # test location attributes
    assert location.id is not None
    assert location.name == "test_location"
    assert location.map == "test_map"
    assert location.map_id == 1

    # test location methods
    assert location.to_json() == '{"id": "' + location.id.hex + \
        '", "_collection": "locations", "_cls": "Location", "name": "test_location", ' + \
        '"map": "test_map", "map_id": 1}'

    # test location equality
    assert location == Location(
        name="test_location",
        map="test_map",
        map_id=1,
    )


def test_station():
    # test construction of the station
    station = Station(
        name="test_station",
        location=Location(
            name="test_location",
            map="test_map",
            map_id=1,
        ),
    )

    # test station attributes
    assert station.id is not None
    assert station.name == "test_station"
    assert station.location.name == "test_location"
    assert station.location.map == "test_map"
    assert station.location.map_id == 1
    assert station.stock == None

    # test station methods
    assert station.to_json() == '{"id": "' + station.id.hex + \
        '", "_collection": "stations", "_cls": "Station", "name": "test_station", ' + \
        '"location": {"id": "' + station.location.id.hex + '", "_collection": "locations", "_cls": "Location", ' + \
        '"name": "test_location", "map": "test_map", "map_id": 1}, "stock": null}'


def test_work_station():
    # test construction of the work station
    work_station = WorkStation(
        name="test_work_station",
        location=Location(
            name="test_location",
            map="test_map",
            map_id=1,
        ),
    )

    # test work station attributes
    assert work_station.id is not None
    assert work_station.name == "test_work_station"
    assert work_station.location.name == "test_location"
    assert work_station.location.map == "test_map"
    assert work_station.location.map_id == 1
    assert work_station.stock == None
    assert work_station.devices == []

    # test work station methods
    assert work_station.to_json() == '{"id": "' + work_station.id.hex + \
        '", "_collection": "stations", "_cls": "WorkStation", "name": "test_work_station", ' + \
        '"location": {"id": "' + work_station.location.id.hex + '", "_collection": "locations", "_cls": "Location", ' + \
        '"name": "test_location", "map": "test_map", "map_id": 1}, "stock": null, "devices": []}'


def test_storage_station():
    # test construction of the storage station
    storage_station = StorageStation(
        name="test_storage_station",
        location=Location(
            name="test_location",
            map="test_map",
            map_id=1,
        ),
    )

    # test storage station attributes
    assert storage_station.id is not None
    assert storage_station.name == "test_storage_station"
    assert storage_station.location.name == "test_location"
    assert storage_station.location.map == "test_map"
    assert storage_station.location.map_id == 1
    assert storage_station.stock == None

    # test storage station methods
    assert storage_station.to_json() == '{"id": "' + storage_station.id.hex + \
        '", "_collection": "stations", "_cls": "StorageStation", "name": "test_storage_station", ' + \
        '"location": {"id": "' + storage_station.location.id.hex + '", "_collection": "locations", "_cls": "Location", ' + \
        '"name": "test_location", "map": "test_map", "map_id": 1}, "stock": null}'


def test_lab():
    # test construction of the lab
    lab = Lab()

    # test lab attributes
    assert lab.stations == []
    assert lab.agents == []

    # test lab methods
    assert lab.to_json() == '{"id": "' + lab.id.hex + \
        '", "_collection": "labs", "_cls": "Lab", "stations": [], "agents": []}'
