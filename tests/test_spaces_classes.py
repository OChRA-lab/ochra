from ochra_common.spaces.location import Location
from ochra_common.spaces.station import Station
from ochra_common.spaces.work_station import WorkStation
from ochra_common.spaces.mobile_station import MobileStation
from ochra_common.spaces.storage_station import StorageStation
from ochra_common.utils.enum import ActiveStatus


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
    assert station.status == ActiveStatus.IDLE
    assert station.locked_by == ""
    assert station.inventory == None

    # test station methods

    assert station.model_dump() == {
        "id": station.id,
        "collection": None,
        "cls": "Station",
        "module_path": None,
        "name": "test_station",
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
        "status": ActiveStatus.IDLE,
        "locked_by": "",
        "inventory": None,
    }


def test_work_station():
    # test construction of the work station
    work_station = WorkStation(
        name="test_work_station",
        location=Location(
            lab="ACL",
            room="main_lab",
            place="bench_1",
        ),
    )

    # test work station attributes
    assert work_station.id is not None
    assert work_station.name == "test_work_station"
    assert work_station.devices == []

    # test work station methods
    assert work_station.model_dump() == {
        "id": work_station.id,
        "collection": None,
        "cls": "WorkStation",
        "module_path": None,
        "name": "test_work_station",
        "location": {
            "id": work_station.location.id,
            "collection": None,
            "cls": "Location",
            "module_path": None,
            "lab": "ACL",
            "room": "main_lab",
            "place": "bench_1",
            "landmarks": [],
            "additional_metadata": {},
        },
        "status": ActiveStatus.IDLE,
        "locked_by": "",
        "inventory": None,
        "devices": [],
    }


def test_storage_station():
    # test construction of the storage station
    storage_station = StorageStation(
        name="test_storage_station",
        location=Location(
            lab="ACL",
            room="storage_room",
            place="cupboard_1",
        ),
    )

    # test storage station attributes
    assert storage_station.id is not None
    assert storage_station.name == "test_storage_station"

    # test storage station methods
    assert storage_station.model_dump() == {
        "id": storage_station.id,
        "collection": None,
        "cls": "StorageStation",
        "module_path": None,
        "name": "test_storage_station",
        "location": {
            "id": storage_station.location.id,
            "collection": None,
            "cls": "Location",
            "module_path": None,
            "lab": "ACL",
            "room": "storage_room",
            "place": "cupboard_1",
            "landmarks": [],
            "additional_metadata": {},
        },
        "status": ActiveStatus.IDLE,
        "locked_by": "",
        "inventory": None,
    }

def test_mobile_station():
    # test construction of the mobile station
    mobile_station = MobileStation(
        name="test_mobile_station",
        location=Location(
            lab="ACL",
            room="main_lab",
            place="bench_1",
        ),
    )

    # test work station attributes
    assert mobile_station.id is not None
    assert mobile_station.name == "test_mobile_station"
    assert mobile_station.mobile_robot == None

    # test work station methods
    assert mobile_station.model_dump() == {
        "id": mobile_station.id,
        "collection": None,
        "cls": "MobileStation",
        "module_path": None,
        "name": "test_mobile_station",
        "location": {
            "id": mobile_station.location.id,
            "collection": None,
            "cls": "Location",
            "module_path": None,
            "lab": "ACL",
            "room": "main_lab",
            "place": "bench_1",
            "landmarks": [],
            "additional_metadata": {},
        },
        "status": ActiveStatus.IDLE,
        "locked_by": "",
        "inventory": None,
        "mobile_robot": None,
    }
