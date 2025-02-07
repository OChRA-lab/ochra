from ochra_common.base import DataModel
from ochra_common.storage.inventory import Inventory
from ochra_common.storage.consumable import Consumable
from ochra_common.storage.container import Container
from ochra_common.storage.holder import Holder
from ochra_common.storage.vessel import Vessel
from ochra_common.storage.reagent import Reagent
from ochra_common.utils.enum import PhysicalState

import uuid


def test_inventory():
    # test construction of the inventory
    station_id = uuid.uuid4()
    owner_station = DataModel(id=station_id, collection="stations", cls="Station")

    inventory = Inventory(owner=owner_station, containers_max_capacity=100)

    # test inventory attributes
    assert inventory.containers == []
    assert inventory.consumables == []
    assert inventory.containers_max_capacity == 100

    # test inventory methods
    assert (
        inventory.model_dump_json()
        == '{"id":"'
        + str(inventory.id)
        + '","collection":null'
        + ',"cls":"Inventory","module_path":null,'
        + '"owner":{"id":"'
        + str(station_id)
        + '","collection":"stations","cls":"Station","module_path":null}'
        + ',"containers_max_capacity":100'
        + ',"containers":[],"consumables":[]}'
    )

    assert inventory.model_dump() == {
        "id": inventory.id,
        "collection": None,
        "cls": "Inventory",
        "module_path": None,
        "owner": {
            "id": station_id,
            "collection": "stations",
            "cls": "Station",
            "module_path": None,
        },
        "containers": [],
        "consumables": [],
        "containers_max_capacity": 100,
    }


def test_consumables():
    # test construction of the consumable
    consumable = Consumable(type="cap", quantity=10)

    # test consumable attributes
    assert consumable.type == "cap"
    assert consumable.quantity == 10

    # test consumable methods
    assert (
        consumable.model_dump_json()
        == '{"id":"'
        + str(consumable.id)
        + '","collection":null,'
        + '"cls":"Consumable","module_path":null,"type":"cap","quantity":10}'
    )

    assert consumable.model_dump() == {
        "id": consumable.id,
        "collection": None,
        "cls": "Consumable",
        "module_path": None,
        "type": "cap",
        "quantity": 10,
    }


def test_container():
    # test construction of the container
    container = Container(type="box", max_capacity=100, physical_id=1)

    # test container attributes
    assert container.type == "box"
    assert container.max_capacity == 100
    assert container.physical_id == 1
    assert not container.is_used

    # test container methods
    assert (
        container.model_dump_json()
        == '{"id":"'
        + str(container.id)
        + '","collection":null,'
        + '"cls":"Container","module_path":null,"type":"box"'
        + ',"max_capacity":100,"physical_id":1,"is_used":false}'
    )

    assert container.model_dump() == {
        "id": container.id,
        "collection": None,
        "cls": "Container",
        "module_path": None,
        "type": "box",
        "physical_id": 1,
        "max_capacity": 100,
        "is_used": False,
    }


def test_holder():
    # test construction of the holder
    holder = Holder(type="rack", max_capacity=16, physical_id=1)

    # test holder attributes
    assert holder.type == "rack"
    assert holder.max_capacity == 16
    assert holder.physical_id == 1
    assert not holder.is_used

    # test holder methods
    assert (
        holder.model_dump_json()
        == '{"id":"'
        + str(holder.id)
        + '","collection":null,'
        + '"cls":"Holder","module_path":null,"type":"rack"'
        + ',"max_capacity":16,"physical_id":1,"is_used":false,"containers":[]}'
    )

    assert holder.model_dump() == {
        "id": holder.id,
        "collection": None,
        "cls": "Holder",
        "module_path": None,
        "type": "rack",
        "physical_id": 1,
        "max_capacity": 16,
        "is_used": False,
        "containers": [],
    }


def test_vessel():
    # test construction of the vessel
    vessel = Vessel(type="vial", max_capacity=5.0, capacity_unit="ml", physical_id=1)

    # test vessel attributes
    assert vessel.type == "vial"
    assert vessel.max_capacity == 5.0
    assert vessel.physical_id == 1
    assert not vessel.is_used

    # test vessel methods
    assert (
        vessel.model_dump_json()
        == '{"id":"'
        + str(vessel.id)
        + '","collection":null,'
        + '"cls":"Vessel","module_path":null,"type":"vial"'
        + ',"max_capacity":5.0,"physical_id":1,"is_used":false,"capacity_unit":"ml"'
        + ',"reagents":[]}'
    )

    assert vessel.model_dump() == {
        "id": vessel.id,
        "collection": None,
        "cls": "Vessel",
        "module_path": None,
        "type": "vial",
        "physical_id": 1,
        "max_capacity": 5.0,
        "is_used": False,
        "capacity_unit": "ml",
        "reagents": [],
    }


def test_reagent():
    # test construction of the reagent
    reagent = Reagent(name="water", amount=100.0, unit="ml")

    # test reagent attributes
    assert reagent.name == "water"
    assert reagent.amount == 100.0
    assert reagent.unit == "ml"
    assert reagent.physical_state == PhysicalState.UNKNOWN
    assert reagent.properties == {}

    # test reagent methods
    assert (
        reagent.model_dump_json()
        == '{"id":"'
        + str(reagent.id)
        + '","collection":null,'
        + '"cls":"Reagent","module_path":null,"name":"water","amount":100.0'
        + ',"unit":"ml","physical_state":-1,"properties":{}}'
    )

    assert reagent.model_dump() == {
        "id": reagent.id,
        "collection": None,
        "cls": "Reagent",
        "module_path": None,
        "name": "water",
        "amount": 100.0,
        "unit": "ml",
        "physical_state": PhysicalState.UNKNOWN,
        "properties": {},
    }
