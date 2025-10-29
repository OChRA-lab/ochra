from ochra_common.spaces.location import Location
from ochra_common.spaces.station import Station
from ochra_common.utils.enum import ActivityStatus, StationType


def test_location():
    # test construction of the location
    location = Location(
        lab="ACL",
        room="main_lab",
        place="bench_1",
        landmarks=["QR123"],
        additional_metadata={"map_id": 1},
    )

    # test location attributes
    assert location.id is not None
    assert location.lab == "ACL"
    assert location.room == "main_lab"
    assert location.place == "bench_1"
    assert location.landmarks == ["QR123"]
    assert location.additional_metadata == {"map_id": 1}

    # test location methods
    assert location.model_dump_json() == (
        '{"id":"'
        + str(location.id)
        + '","collection":null'
        + ',"cls":"Location","module_path":null,'
        + '"lab":"ACL","room":"main_lab","place":"bench_1",'
        + '"landmarks":["QR123"],"additional_metadata":{"map_id":1}}'
    )

    # test location equality
    assert location == Location(
        lab="ACL",
        room="main_lab",
        place="bench_1",
        landmarks=["QR123"],
        additional_metadata={"map_id": 1},
    )


def test_station():
    # test construction of the station
    station = Station(
        name="test_station",
        type=StationType.WORK_STATION,
        location=Location(
            lab="ACL",
            room="main_lab",
            place="bench_1",
        ),
    )

    # test station attributes
    assert station.id is not None
    assert station.name == "test_station"
    assert station.location.lab == "ACL"
    assert station.location.room == "main_lab"
    assert station.location.place == "bench_1"
    assert station.type == StationType.WORK_STATION
    assert station.status == ActivityStatus.IDLE
    assert station.locked_by == ""
    assert station.inventory == None
    assert station.devices == []

    # test station methods

    assert station.model_dump() == {
        "id": station.id,
        "collection": None,
        "cls": "Station",
        "module_path": None,
        "name": "test_station",
        "type": StationType.WORK_STATION,
        "location": {
            "id": station.location.id,
            "collection": None,
            "cls": "Location",
            "module_path": None,
            "lab": "ACL",
            "room": "main_lab",
            "place": "bench_1",
            "landmarks": [],
            "additional_metadata": {},
        },
        "status": ActivityStatus.IDLE,
        "locked_by": "",
        "inventory": None,
        "devices": [],
    }
